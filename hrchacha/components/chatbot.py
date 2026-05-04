import sys

import streamlit as st

from hrchacha.components.data_handler import Database
from hrchacha.components.llm_handler import LLM
from hrchacha.constants import BOT_ROLE
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging


class HRChacha:
    def __init__(self):
        self.message_history = st.session_state.chat_messages

        if "llm" not in st.session_state:
            st.session_state.llm = LLM()

        if "database" not in st.session_state:
            st.session_state.database = Database()

        self.llm = st.session_state.llm
        self.db = st.session_state.database

    def stream_chat_response(self):
        """Stream chat response and save to messages."""
        try:
            full_response = st.write_stream(self.llm.stream_chat_response())
            if not full_response:
                st.error("The chat model returned an empty response. Please try again.")
                return

            st.session_state.chat_messages.append({
                "role": BOT_ROLE,
                "content": full_response
            })

            # Auto-complete when closing message is delivered
            if "Your application is complete" in full_response:
                st.session_state.processing_status = "not_started"
                st.session_state.conversation_processed = False
                st.session_state.current_screen = "processing"
                st.rerun()

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            st.error("Chat error. Please try again.")

    def process_conversation(self):
        """Extract data with Summary LLM and save to MongoDB."""
        try:
            messages = [
                f"{msg['role']}: {msg['content']}"
                for msg in st.session_state.chat_messages
                if msg["role"] in ("user", "assistant")
            ]
            conversation = "\n".join(messages)

            logging.info(
                "Processing completed conversation. message_count=%d conversation_chars=%d",
                len(messages),
                len(conversation),
            )

            candidate_data = self.llm.extract_candidate_data(conversation)
            st.session_state.last_processed_email = candidate_data.get("email")
            candidate_data["session_chat"] = st.session_state.chat_messages

            logging.info(
                "Candidate data ready for MongoDB upload. email=%s top_level_keys=%s",
                candidate_data.get("email"),
                sorted(candidate_data.keys()),
            )
            saved = self.db.insert_user(candidate_data)
            if not saved:
                logging.error(
                    "MongoDB upload was not acknowledged. email=%s",
                    candidate_data.get("email"),
                )
                st.error("Failed to save data to MongoDB. Please try again.")
                return False

            logging.info("Candidate data saved successfully. email=%s", candidate_data.get("email"))
            st.success("✅ Data processed and saved!")
            return True

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.exception("Conversation processing failed. error_type=%s", type(e).__name__)
            logging.error(str(err))
            st.error("Processing failed.")
            return False
