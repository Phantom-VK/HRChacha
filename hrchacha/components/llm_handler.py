import logging
import sys
from typing import Optional, Any, Iterator

import streamlit as st
from groq import Groq
from pydantic import BaseModel, EmailStr
from typing import List

from hrchacha.constants import CHAT_MODEL, SUMMARY_MODEL
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.utils.general_utils import get_secret


class CandidateData(BaseModel):
    email: Optional[str] = None
    candidate_information: dict = {}
    technical_assessment: dict = {}


class LLM:
    def __init__(self):
        api_key = get_secret("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def get_chat_response(self, stream: bool = True) -> Optional[Any]:
        """Chat LLM streaming response."""
        try:
            messages = st.session_state.chat_messages
            return self.client.chat.completions.create(
                messages=messages,
                model=CHAT_MODEL,
                stream=stream,
                max_tokens=512,
                temperature=0.3,
                top_p=0.8,
            )
        except Exception as e:
            logging.error(f"Chat LLM error: {e}")
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
                    {"role": "user", "content": prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "user_information",
                        "description": "User information extracted from the chat conversation",
                        "schema": CandidateData.model_json_schema()

                    }},
                temperature=0.1,
                max_tokens=2000
            )

            content = response.choices[0].message.content.strip()

            # Extract JSON from USER_DATA block
            import json, re
            json_match = re.search(r'``````', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            return json.loads(content) if content.startswith('{') else None

        except Exception as e:
            logging.error(f"Summary LLM error: {e}")
            return None
