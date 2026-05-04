import json
import sys
from typing import Dict, List, Optional, Any, Generator

import streamlit as st
from openai import OpenAI
from pydantic import BaseModel, EmailStr, Field

from hrchacha.constants import CHAT_MODEL, SYSTEM_ROLE
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging
from hrchacha.prompts import EXTRACTION_SYSTEM_PROMPT
from hrchacha.utils.general_utils import get_secret


# ── Pydantic models ────────────────────────────────────────────────────────────

class CandidateInformation(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    professional_experience: Optional[str] = None
    non_professional_experience: Optional[str] = None
    desired_positions: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    technical_skills: List[str] = Field(default_factory=list)


class CandidateData(BaseModel):
    email: Optional[EmailStr] = None
    candidate_information: CandidateInformation = Field(default_factory=CandidateInformation)
    technical_assessment: Dict[str, str] = Field(default_factory=dict)


# ── LLM class ─────────────────────────────────────────────────────────────────

class LLM:
    def __init__(self):
        api_key = get_secret("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is required.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
        )

    @staticmethod
    def _trim_messages(
        messages: list,
        max_messages: int = 24,
        max_message_chars: int = 6000,
        max_total_chars: int = 30000,
    ) -> list:
        """Keep the latest context without sending oversized payloads."""
        system_msgs = [m for m in messages if m["role"] == SYSTEM_ROLE]
        non_system  = [m for m in messages if m["role"] != SYSTEM_ROLE]

        trimmed = []
        total_chars = 0

        for message in reversed(non_system[-max_messages:]):
            content = message.get("content", "")

            if len(content) > max_message_chars:
                content = content[:max_message_chars] + "\n\n[Truncated]"

            if total_chars + len(content) > max_total_chars:
                remaining = max_total_chars - total_chars
                if remaining <= 0:
                    break
                content = content[:remaining] + "\n\n[Truncated]"

            trimmed.append({**message, "content": content})
            total_chars += len(content)

        trimmed.reverse()
        return ([system_msgs[0]] if system_msgs else []) + trimmed

    def stream_chat_response(self) -> Generator[str | None | Any, Any, None]:
        """Stream DeepSeek chat tokens back to the caller."""
        messages = self._trim_messages(st.session_state.chat_messages)

        response = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            stream=True,
            max_tokens=800,
            temperature=0.3,
            top_p=0.8,
        )

        received_content = False
        finish_reason = None

        for chunk in response:
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            finish_reason = choice.finish_reason or finish_reason
            delta = getattr(choice.delta, "content", None)
            if delta:
                received_content = True
                yield delta

        if finish_reason == "length":
            yield "\n\nI reached the response limit. Reply with `continue` and I'll proceed."

        if not received_content:
            raise RuntimeError("DeepSeek returned an empty streamed response.")

    def extract_candidate_data(self, conversation: str) -> dict:
        """Use DeepSeek to extract structured candidate data from the conversation."""
        try:
            logging.info("Starting candidate extraction. conversation_chars=%d", len(conversation))

            response = self.client.chat.completions.create(
                model=CHAT_MODEL,
                messages=[
                    {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                    {"role": "user",   "content": f"Extract from this conversation:\n\n{conversation}"},
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=4000,
            )

            choice  = response.choices[0]
            content = (choice.message.content or "").strip()

            if not content:
                raise ValueError("DeepSeek extraction returned empty content.")

            # Guard: if model was still cut off, trim to last valid closing brace
            if choice.finish_reason == "length":
                logging.warning("Extraction hit max_tokens limit — attempting JSON repair.")
                last_brace = content.rfind("}")
                if last_brace == -1:
                    raise ValueError("Response was truncated and no valid JSON object found.")
                content = content[:last_brace + 1]

            candidate_data = json.loads(content)
            validated      = CandidateData.model_validate(candidate_data)
            normalized     = validated.model_dump(mode="json")

            logging.info(
                "Extraction complete. email=%s skills=%d",
                normalized.get("email"),
                len((normalized.get("candidate_information") or {}).get("technical_skills") or []),
            )
            return normalized

        except Exception as e:
            logging.exception("Candidate extraction failed. error_type=%s", type(e).__name__)
            raise HRChachaException(e, sys)