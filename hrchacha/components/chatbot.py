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

    def _close_resources(self):
        try:
            if hasattr(self.db, "client"):
                self.db.client.close()
        except Exception:
            pass

    def get_response_stream(self):
        """Get chat LLM streaming response."""
        return self.llm.get_chat_response(stream=True)

    def stream_chat_response(self):
        """Stream chat response and save to messages."""
        try:
            response_stream = self.get_response_stream()
            if response_stream is None:
                st.error("Chat service unavailable. Please try again in a moment.")
                return

            full_response = ""

            def content_generator():
                nonlocal full_response
                for chunk in response_stream:
                    # Groq streaming chunks
                    delta = None
                    try:
                        delta = chunk.choices[0].delta.content
                    except Exception:
                        # Handle plain strings (non-stream mode) or other iterables
                        if isinstance(chunk, str):
                            delta = chunk
                    if delta:
                        full_response += delta
                        yield delta

            if hasattr(response_stream, "__iter__") and not isinstance(response_stream, str):
                st.write_stream(content_generator())
            else:
                # Non-streamed full response
                msg_content = getattr(response_stream, "choices", None)
                if msg_content:
                    full_response = response_stream.choices[0].message.content
                    st.write(full_response)
                elif isinstance(response_stream, str):
                    full_response = response_stream
                    st.write(full_response)

            # Save to session
            st.session_state.chat_messages.append({
                "role": BOT_ROLE,
                "content": full_response
            })

            # Auto-complete when closing message is delivered
            if "Your application is complete" in full_response:
                st.session_state.current_screen = "processing"
                st.rerun()

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
                if msg["role"] in ("user", "assistant")
            ])

            logging.info("Extracting candidate data...")

            # Extract structured data
            candidate_data = self.llm.extract_candidate_data(conversation)
            if not candidate_data:
                st.error("Failed to process data. Please try again.")
                return

            # Save to MongoDB
            st.session_state.last_processed_email = candidate_data.get("email")
            candidate_data["session_chat"] = st.session_state.chat_messages
            self.db.insert_user(candidate_data)

            logging.info("Candidate data saved successfully!")
            st.success("✅ Data processed and saved!")

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            st.error("Processing failed.")
        finally:
            self._close_resources()
