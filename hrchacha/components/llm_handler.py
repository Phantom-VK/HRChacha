import logging
import sys
from typing import Optional, Any

import streamlit as st
from groq import Groq

from hrchacha.exceptions.exception import HRChachaException
from hrchacha.utils.general_utils import get_secret


class LLM:
    """
    LLM wrapper using Groq's chat completions API (LLaMA via Groq).

    Usage:
        llm = LLM()
        # streaming:
        stream_iter = llm.get_llama_response(stream=True)
        for chunk in stream_iter:
            # chunk handling depends on Groq's streaming object shape
            ...
        # non-streaming:
        text = llm.get_llama_response(stream=False)
    """

    DEFAULT_MODEL = "llama-3.3-70b-versatile"

    def __init__(self):
        try:
            api_key = get_secret("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY must be defined as a Streamlit secret or environment variable.")
            self.client = Groq(api_key=api_key)

        except Exception as e:
            print(f"API Key error: {e}")

    def get_llama_response(self, *, stream: bool = True, model: Optional[str] = None) -> Optional[Any]:
        """
        Request a chat completion from Groq.

        If `stream=True`, this function returns the streaming iterator object
        produced by the Groq SDK (if the SDK supports streaming). If streaming
        is not supported, it will fall back to returning the full response.

        If `stream=False`, returns the final text response (string) or None on error.

        Uses `st.session_state.messages` as the messages payload (same structure).
        """
        model = model or self.DEFAULT_MODEL

        try:
            messages = st.session_state.get("messages", [])
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                stream=stream,
                temperature=0.4,
                top_p=0.9,
            )

            if stream:
                return response

            if hasattr(response, "choices") and len(response.choices) > 0:
                return response.choices[0].message.content
            if isinstance(response, dict):
                # try to pull out content if present
                choices = response.get("choices", [])
                if choices:
                    first = choices[0]
                    msg = first.get("message") or first.get("text") or {}
                    if isinstance(msg, dict):
                        return msg.get("content") or msg.get("text")
                    return msg
            return None

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return None
