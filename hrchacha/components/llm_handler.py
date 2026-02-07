import logging
import sys
from typing import Optional, Any, Dict, List

import streamlit as st
from groq import Groq
from pydantic import BaseModel, EmailStr, Field

from hrchacha.constants import CHAT_MODEL, SUMMARY_MODEL
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.utils.general_utils import get_secret


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


class LLM:
    def __init__(self):
        groq_api_key = get_secret("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is required for chat and summary.")
        self.client = Groq(api_key=groq_api_key)

    def get_chat_response(self, stream: bool = True) -> Optional[Any]:
        """Chat LLM response; returns full text or a token generator if stream=True."""
        try:
            messages = st.session_state.chat_messages
            response = self.client.chat.completions.create(
                messages=messages,
                model=CHAT_MODEL,
                stream=stream,
                max_tokens=512,
                temperature=0.3,
                top_p=0.8,
            )
            return response
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return None

    def extract_candidate_data(self, conversation: str) -> Optional[dict]:
        """Summary LLM extracts structured JSON from conversation."""
        try:
            from hrchacha.prompts import SUMMARY_MODEL_MESSAGE

            prompt = SUMMARY_MODEL_MESSAGE.format(CONVERSATION_HISTORY=conversation)

            response = self.client.chat.completions.create(
                model=SUMMARY_MODEL,
                messages=[
                    {"role": "system", "content": "Extract candidate data into JSON only."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=2000,
                stream=False,
            )
            content = response.choices[0].message.content.strip()

            # Extract JSON from USER_DATA block
            import json, re
            json_match = re.search(r'```json\\s*(.*?)\\s*```', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback: grab first JSON object in the text
                first = content.find("{")
                last = content.rfind("}")
                if first != -1 and last != -1 and last > first:
                    return json.loads(content[first:last + 1])
                return None
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return None
