import sys
import streamlit as st
from hrchacha.components.chatbot import HRChacha
from hrchacha.constants import BOT_ROLE, USER_ROLE
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging
from hrchacha.prompts import SYSTEM_PROMPT, INITIAL_GREETING_MESSAGE, CHATBOT_REFERENCE_QUESTIONS
from hrchacha.utils.general_utils import get_random_chacha_thinking_line


class ChatUI:
    def __init__(self, title: str):
        self.title = title
        self._initialize_state()

    def _initialize_state(self):
        """Initializes session state for chat."""
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {"role": BOT_ROLE, "content": SYSTEM_PROMPT},
                {"role": BOT_ROLE, "content": CHATBOT_REFERENCE_QUESTIONS},
                {"role": BOT_ROLE, "content": INITIAL_GREETING_MESSAGE}
            ]

        if "chat_bot" not in st.session_state:
            st.session_state.chat_bot = HRChacha()

    def render(self):
        st.markdown(
            """
            <div style="display:flex; align-items:center; justify-content:space-between;">
                <h2>💬 HRChacha</h2>
                <span style="color:#94a3b8;">Hiring Assistant</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("End Chat", use_container_width=True):
                st.session_state.current_screen = "processing"
                st.rerun()

        self._display_chat_messages()
        self._chat_input()

    def _display_chat_messages(self):
        """Displays all chat messages."""
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                if (message["role"] == BOT_ROLE and
                        message["content"] in [SYSTEM_PROMPT, CHATBOT_REFERENCE_QUESTIONS]):
                    continue

                avatar = "user" if message["role"] == USER_ROLE else "ai"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

    def _chat_input(self):
        """Handles user input."""
        if prompt := st.chat_input("Ask HRChacha anything about hiring..."):
            self._process_user_input(prompt)

    def _process_user_input(self, prompt: str):
        """Process chat with separate LLMs."""
        try:
            print("Processing user input...", prompt)
            # Add user message
            st.session_state.chat_messages.append({"role": USER_ROLE, "content": prompt})

            with st.chat_message(USER_ROLE):
                st.markdown(prompt)

            # Chat LLM response
            with st.chat_message(BOT_ROLE):
                st.session_state.chat_bot.stream_chat_response()  # Uses CHAT_MODEL

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            st.error("Sorry, something went wrong. Please try again.")
