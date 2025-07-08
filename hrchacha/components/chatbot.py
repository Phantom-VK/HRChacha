from typing import List

import streamlit as st

from hrchacha.constants import ConversationState, User, Job, GreetingMessage


class HRChacha:

    def __init__(self):
        self.state = ConversationState.GREETING
        self.user = User()
        self.message_history = st.session_state.messages

        if "new_user" not in st.session_state:
            st.session_state.new_user = True
        if "new_interaction" not in st.session_state:
            st.session_state.new_interaction = True


    def get_response(self, prompt:str) -> str | None:
        if self.state == ConversationState.GREETING and st.session_state.new_user :
            st.session_state.new_user = False
            st.session_state.new_interaction = False
            return GreetingMessage.get_main_greeting()
        return GreetingMessage.get_welcome_back_message()


    def validate_user_info(self) -> (bool, str):
        pass

    def generate_questions(self):
        pass

    def suggest_jobs(self) -> List[Job]:
        pass

