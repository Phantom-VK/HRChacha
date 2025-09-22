import random
import os
from hrchacha.constants import HR_CHACHA_THINKING_LINES
from dotenv import load_dotenv
load_dotenv()

def get_random_chacha_thinking_line() -> str:
    return random.choice(HR_CHACHA_THINKING_LINES)



def get_secret(key):
    # Try st.secrets if running inside Streamlit and the key exists
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except ImportError:
        # Not running in Streamlit, skip
        pass
    # Fallback to environment variable
    return os.getenv(key)
