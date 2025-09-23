import random
import os
from hrchacha.constants import HR_CHACHA_THINKING_LINES
from hrchacha.logging.logger import logging
from dotenv import load_dotenv
import streamlit as st

def get_random_chacha_thinking_line() -> str:
    return random.choice(HR_CHACHA_THINKING_LINES)



def get_secret(key):
    load_dotenv()
    try:
        key = os.getenv(key)
        if key:
            logging.info(f"Found environmental secret key!")
            return key
    except ValueError:
        pass
    logging.info(f"No secret key found, using streamlit key")
    return st.secrets.get(key)
