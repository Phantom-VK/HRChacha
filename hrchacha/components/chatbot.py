import json
import re
import sys
import time

import streamlit as st

from hrchacha.components.llm_handler import LLM
from hrchacha.constants import BOT_ROLE
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging


class HRChacha:

    def __init__(self):
        self.message_history = st.session_state.messages
        self.llm = LLM()

        if "user_interactions" not in st.session_state:
            st.session_state.user_interactions = 0


    def get_response_stream(self) -> str:
        try:

            return self.llm.get_llama_response()

        except Exception as e:
            raise HRChachaException(e, sys)

    def _extract_user_info(self, corpus) -> str:
        try:
            logging.info("Extracting user info from EXTRACT101 message...")

            match = re.search(r'USER_DATA.*?({.*})', corpus, re.DOTALL)
            if not match:
                raise ValueError("No JSON object found in the message.")

            json_str = match.group(1)

            user_data = json.loads(json_str)

            # Save to DB
            # self.save_to_db(user_data)

            logging.info("User data extracted successfully.")
            return f"✅ User data saved:\n\n```json\n{json.dumps(user_data, indent=2)}\n```"

        except Exception as e:
            logging.error(f"Error extracting user info: {e}")
            raise HRChachaException(e, sys)

    def stream_and_capture_response(self, response_generator):
        try:
            logging.info("Streaming and capturing response...")

            response_box = st.empty()

            full_response = ""

            stream_container = ""

            for chunk in response_generator:
                if hasattr(chunk, "choices"):
                    delta = chunk.choices[0].delta.content
                    if delta:

                        full_response += delta
                        stream_container += delta
                        response_box.markdown(stream_container)
                        time.sleep(0.01)

            response_box.markdown(full_response)

            st.session_state.messages.append({
                "role": BOT_ROLE,
                "content": full_response
            })

            if "USER_DATA" in full_response:
                extracted_result = self._extract_user_info(full_response)

                st.session_state.user_data = extracted_result

                print(st.session_state.user_data)

        except Exception as e:
            raise HRChachaException(e, sys)








