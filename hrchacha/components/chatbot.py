import logging
import sys

import streamlit as st

from hrchacha.components.data_handler import Database
from hrchacha.components.llm_handler import LLM
from hrchacha.constants import BOT_ROLE
from hrchacha.exceptions.exception import HRChachaException


class HRChacha:
    def __init__(self):
        self.message_history = st.session_state.chat_messages

        if "llm" not in st.session_state:
            st.session_state.llm = LLM()

        if "database" not in st.session_state:
            st.session_state.database = Database()

        self.llm = st.session_state.llm
        self.db = st.session_state.database

    def get_response_stream(self):
        """Get chat LLM streaming response."""
        return self.llm.get_chat_response(stream=True)

    def stream_chat_response(self):
        """Stream chat response and save to messages."""
        try:
            response_stream = self.get_response_stream()
            if not response_stream:
                return

            full_response = ""

            # Stream response
            def content_generator():
                nonlocal full_response
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        delta = chunk.choices[0].delta.content
                        full_response += delta
                        yield delta

            st.write_stream(content_generator())

            # Save to session
            st.session_state.chat_messages.append({
                "role": BOT_ROLE,
                "content": full_response
            })

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            st.error("Chat error. Please try again.")

    def process_conversation(self):
        """Extract data with Summary LLM and save to MongoDB."""
        try:
            # Get full conversation
            conversation = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in st.session_state.chat_messages
            ])

            logging.info("Extracting candidate data...")

            # Extract structured data
            candidate_data = self.llm.extract_candidate_data(conversation)
            if not candidate_data:
                st.error("Failed to process data. Please try again.")
                return

            # Save to MongoDB
            candidate_data["session_chat"] = st.session_state.chat_messages
            self.db.insert_user(candidate_data)

            logging.info("Candidate data saved successfully!")
            st.success("✅ Data processed and saved!")

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            st.error("Processing failed.")
