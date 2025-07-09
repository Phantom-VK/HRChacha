import sys

import streamlit as st
from hrchacha.constants import USER_CHAT_INPUT_KEY
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.ui.main_window import MainWindowUI
from hrchacha.logging.logger import logging

def custom_response_handler(prompt: str) -> str:
    """Custom logic for generating bot responses.

    Args:
        prompt: The user's input message

    Returns:
        The bot's response
    """
    return f"You said: {prompt}. This is a custom response!"


if __name__ == "__main__":
    try:
        logging.info("Started Chatbot")
        main_app = MainWindowUI(
                title=" HRChacha – Your Tech Job Buddy",
                response_callback=custom_response_handler
            )


        if prompt := st.chat_input("What's up?", key=USER_CHAT_INPUT_KEY):
                main_app.process_user_input(prompt)
    except Exception as e:
        raise HRChachaException(e, sys)