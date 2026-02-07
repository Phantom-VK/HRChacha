import os
import random

import streamlit as st
from dotenv import load_dotenv

from hrchacha.constants import HR_CHACHA_THINKING_LINES
from hrchacha.logging.logger import logging


def get_random_chacha_thinking_line() -> str:
    return random.choice(HR_CHACHA_THINKING_LINES)


def get_secret(key: str):
    """Retrieve a secret from env first, then Streamlit secrets without mutating the key."""
    load_dotenv()

    env_val = os.getenv(key)
    if env_val:
        logging.info(f"Using environment secret for {key}")
        return env_val

    streamlit_val = st.secrets.get(key)
    if streamlit_val:
        logging.info(f"Using Streamlit secret for {key}")
        return streamlit_val

    logging.warning(f"Secret {key} not found in environment or Streamlit")
    return None
