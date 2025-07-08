import streamlit as st
from typing import Optional, Callable


class MainWindowUI:
    def __init__(self, title: str, response_callback: Optional[Callable] = None):
        """Initialize the chat UI.

        Args:
            title: Title for the chat window
            response_callback: Optional function to process user input and return bot response
        """
        self.title = title
        self.response_callback = self.default_response

        if "messages" not in st.session_state:
            st.session_state.messages = []

        self.USER_ROLE = "user"
        self.BOT_ROLE = "assistant"

        self._initialize_ui()

    def _initialize_ui(self):
        """Set up the initial UI components."""
        st.set_page_config(page_title=self.title)
        st.title(self.title)

        self._display_messages()


    def _display_messages(self):
        """Display all messages in the chat history."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def process_user_input(self, prompt: str):
        """Handle user input and generate bot response.

        Args:
            prompt: The user's input message
        """
        if not prompt.strip():
            return
        st.session_state.messages.append({"role": self.USER_ROLE, "content": prompt})

        bot_response = self.response_callback(prompt)
        self._display_bot_response(bot_response)

        st.rerun()

    def _display_bot_response(self, response: str):
        """Display the bot's response.

        Args:
            response: The bot's response message
        """
        if response:
            st.session_state.messages.append({
                "role": self.BOT_ROLE,
                "content": f"Bot: {response}"
            })

    @staticmethod
    def default_response(prompt: str) -> str:
        """Default response handler if none provided.

        Args:
            prompt: The user's input message

        Returns:
            A simple echo response
        """
        return prompt