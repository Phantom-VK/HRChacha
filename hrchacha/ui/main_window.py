import sys
import time
from typing import Optional, Callable

import streamlit as st

from hrchacha.components.chatbot import HRChacha
from hrchacha.constants import (
    BOT_ROLE,
    USER_ROLE
)
from hrchacha.prompts import SYSTEM_PROMPT, INITIAL_GREETING_MESSAGE
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging


class MainWindowUI:
    def __init__(self, title: str, response_callback: Optional[Callable] = None):
        self.title = title

        self._initialize_state()
        self._render_ui()

    def _initialize_state(self):
        """Initializes session state variables for chatbot."""
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": BOT_ROLE, "content": SYSTEM_PROMPT},
                {"role": BOT_ROLE, "content": INITIAL_GREETING_MESSAGE}
            ]
            logging.info("Initialized session messages")

        if "user_data" not in st.session_state:
            st.session_state.user_data = ""
            logging.info("Initialized user data")

        if "bot" not in st.session_state:
            st.session_state.bot = HRChacha()
            logging.info("Initialized HRChacha bot")

    def _render_ui(self):
        """Render the chatbot UI."""
        try:
            st.set_page_config(page_title=self.title)
            st.markdown(f"# 👋 {self.title}")
            self._display_all_messages()
        except Exception as e:
            raise HRChachaException(e, sys)

    def _display_all_messages(self):
        """Displays all previous chat messages (except the system prompt)."""
        try:
            for i, message in enumerate(st.session_state.messages):
                if message["role"] == BOT_ROLE and message["content"] == SYSTEM_PROMPT:
                    continue  # skip displaying raw system prompt

                avatar = "🧑" if message["role"] == USER_ROLE else "🤖"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

        except Exception as e:
            raise HRChachaException(e, sys)

    def _stream_response(self, text: str):
        """Yields characters one by one for a typing effect."""
        for char in text:
            yield char
            time.sleep(0.01)

    def process_user_input(self, prompt: str):
        """Processes the user input and triggers the bot's response."""
        try:
            prompt = prompt.strip()
            if not prompt:
                return

            st.session_state.messages.append({
                "role": USER_ROLE,
                "content": prompt
            })

            with st.chat_message(BOT_ROLE, avatar="🤖"):
                thinking = st.empty()
                thinking.markdown("🧠 *HR Chacha is thinking...*")

            response_generator = st.session_state.bot.get_response_stream()

            with st.chat_message(BOT_ROLE, avatar="🤖"):
                st.session_state.bot.stream_and_capture_response(response_generator)

            st.rerun()

        except Exception as e:
            raise HRChachaException(e, sys)
