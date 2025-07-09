from typing import List

import streamlit as st

from hrchacha.logging.logger import logging
from hrchacha.constants import ConversationState, User, Job, GreetingMessage


class HRChacha:

    def __init__(self):
        self.state = ConversationState.GREETING
        self.user = User()
        self.message_history = st.session_state.messages

        if "user_interactions" not in st.session_state:
            st.session_state.user_interactions = 0


    def get_response(self, prompt:str) -> str | None:
        logging.info("Getting bot response")
        if self.state == ConversationState.GREETING:
            if st.session_state.user_interactions == 0:
                st.session_state.new_user = False
                st.session_state.user_interactions += 1
                return GreetingMessage.get_main_greeting()
            else:
                st.session_state.user_interactions += 1
                return GreetingMessage.get_welcome_back_message()
        st.session_state.user_interactions += 1
        return self.process_user_prompt(prompt)


    def validate_user_info(self) -> (bool, str):
        pass

    def generate_questions(self):
        pass

    def suggest_jobs(self) -> List[Job]:
        pass

    def process_user_prompt(self, prompt):

        pass

