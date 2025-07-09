import sys
import time
import streamlit as st
from typing import Optional, Callable

from hrchacha.components.chatbot import HRChacha
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging


class MainWindowUI:
    USER_ROLE = "user"
    BOT_ROLE = "assistant"

    def __init__(self, title: str, response_callback: Optional[Callable] = None):
        """
        Initialize the chat UI.

        Args:
            title (str): Title for the chat window
            response_callback (Callable, optional): Custom function to generate bot responses.
        """
        self.title = title

        self.response_callback = self.default_response


        if "messages" not in st.session_state:
            st.session_state.messages = []
            logging.info("Initialzed session messages")

        if "bot" not in st.session_state:
            st.session_state.bot = HRChacha()
            logging.info("Initialized bot")

        self._render_ui()

    def _render_ui(self):
        """Set up UI layout and render messages."""
        try:
            st.set_page_config(page_title=self.title)
            st.title(self.title)

            self._display_all_messages()
        except Exception as e:
            raise  HRChachaException(e, sys)

    def _display_all_messages(self):

        try:
            messages = st.session_state.get("messages", [])

            if not messages:
                return

            # If there's a streaming message, stream only the last one
            stream_last = st.session_state.get("stream_next", False)

            for i, message in enumerate(messages):
                is_last = i == len(messages) - 1

                with st.chat_message(message["role"]):
                    if is_last and stream_last:
                        st.write_stream(self._stream_response(message["content"]))
                    else:
                        st.markdown(message["content"])

            st.session_state.stream_next = False
        except Exception as e:
            raise HRChachaException(e, sys)

    def _stream_response(self, text: str):
        """Yields the text character by character for a streaming effect."""
        for char in text:
            yield char
            time.sleep(0.01)

    def process_user_input(self, prompt: str):
        logging.info("Processing user input")
        try:
            prompt = prompt.strip()
            if not prompt:
                return

            st.session_state.messages.append({
                "role": self.USER_ROLE,
                "content": prompt
            })

            response = self.response_callback(prompt)

            # Append bot message but mark it to be streamed
            st.session_state.messages.append({
                "role": self.BOT_ROLE,
                "content": response
            })

            st.session_state.stream_next = True
            st.rerun()
        except Exception as e:
            raise HRChachaException(e, sys)

    def default_response(self, prompt: str) -> str:
        """
        Default response generator using HRChacha backend.

        Args:
            prompt (str): User input.

        Returns:
            str: Bot response.
        """
        return st.session_state.bot.get_response(prompt)
