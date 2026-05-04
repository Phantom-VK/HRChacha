import sys
import streamlit as st
from hrchacha.components.chatbot import HRChacha
from hrchacha.constants import BOT_ROLE, USER_ROLE, SYSTEM_ROLE, CHAT_MODEL, SUMMARY_MODEL
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging
from hrchacha.prompts import INITIAL_GREETING_MESSAGE, SYSTEM_PROMPT


class ChatUI:
    def __init__(self, title: str):
        self.title = title
        self._initialize_state()

    def _initialize_state(self):
        """Initializes session state for chat."""
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {"role": SYSTEM_ROLE, "content": SYSTEM_PROMPT},
                {"role": BOT_ROLE, "content": INITIAL_GREETING_MESSAGE},
            ]

        # Only reset processing flag when starting fresh (not on every rerun)
        if "conversation_processed" not in st.session_state:
            st.session_state.conversation_processed = False

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
            unsafe_allow_html=True,
        )

        self._render_badges()
        self._render_sidebar()
        self._display_chat_messages()

        # Spacer so Streamlit's sticky chat input doesn't cover last message
        st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)

        self._chat_input()
        self._render_end_chat_button()

    def _display_chat_messages(self):
        """Displays all non-system chat messages."""
        for message in st.session_state.chat_messages:
            if message["role"] == SYSTEM_ROLE:
                continue
            avatar = "user" if message["role"] == USER_ROLE else "assistant"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    def _chat_input(self):
        """Handles user chat input."""
        if prompt := st.chat_input("Answer the current question or share required details..."):
            self._process_user_input(prompt)

    def _render_end_chat_button(self):
        """
        Floating End Chat button.
        Ends the current interview without processing or saving partial data.
        """
        st.markdown('<div class="end-chat-wrapper">', unsafe_allow_html=True)
        if st.button("End Chat", key="end_chat_fab"):
            database = st.session_state.get("database")
            if database and hasattr(database, "client"):
                database.client.close()

            for key in [
                "chat_messages",
                "chat_bot",
                "conversation_processed",
                "processing_status",
                "last_processed_email",
                "llm",
                "database",
            ]:
                st.session_state.pop(key, None)

            st.session_state.current_screen = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    def _process_user_input(self, prompt: str):
        """Adds user message and gets bot response."""
        try:
            # Append and display user message
            st.session_state.chat_messages.append({"role": USER_ROLE, "content": prompt})
            with st.chat_message(USER_ROLE, avatar="user"):
                st.markdown(prompt)

            with st.chat_message(BOT_ROLE, avatar="assistant"):
                st.session_state.chat_bot.stream_chat_response()  # Uses CHAT_MODEL

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            st.error("Sorry, something went wrong. Please try again.")

    def _render_sidebar(self):
        with st.sidebar:
            st.markdown("### Session Overview")
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-row"><span>🗣️ Chat Model</span><code>{CHAT_MODEL}</code></div>
                    <div class="info-row"><span>🧾 Summary Model</span><code>{SUMMARY_MODEL}</code></div>
                    <div class="info-row"><span>🔐 Data</span><span>Stored in MongoDB only after a complete interview.</span></div>
                    <div class="info-row"><span>⚠️ Privacy</span><span>End Chat discards the current session.</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def _render_badges(self):
        st.markdown(
            """
            <div style="display:flex; gap:8px; flex-wrap:wrap; margin: 0.5rem 0 1rem 0;">
                <span class="pill pill-live">● Live</span>
                <span class="pill pill-phase">Phase 1: Info → Phase 2: Tech → Phase 3: Summary</span>
                <span class="pill pill-llm">Dual LLM Pipeline</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
