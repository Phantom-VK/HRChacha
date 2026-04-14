import streamlit as st

from hrchacha.ui.chat_ui import ChatUI
from hrchacha.ui.home_screen import HomeScreen
from hrchacha.ui.theme import apply_dark_blue_theme


class MainWindowUI:
    def __init__(self):
        # set_page_config MUST be the very first Streamlit call — before any st.markdown or st.write
        st.set_page_config(
            page_title="HRChacha - AI Hiring Assistant by TalentScout",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
        apply_dark_blue_theme()
        self._initialize_app_state()
        self.home_screen = HomeScreen()
        self.chat_ui = ChatUI("HRChacha - TalentScout")

    def _initialize_app_state(self):
        """Initialize the main app state."""
        if "current_screen" not in st.session_state:
            st.session_state.current_screen = "home"
        if "conversation_processed" not in st.session_state:
            st.session_state.conversation_processed = False

    def run(self):
        """Main app runner — handles screen navigation."""
        screen = st.session_state.current_screen

        if screen == "home":
            self.home_screen.render()
        elif screen == "chat":
            self.chat_ui.render()
        elif screen == "processing":
            self._show_processing_screen()

    def _show_processing_screen(self):
        """Process conversation with Summary LLM and save to DB."""
        st.title("⏳ Processing Your Session")
        st.markdown("**HRChacha is extracting your data...**")

        progress_bar = st.progress(0)

        has_chat_bot = "chat_bot" in st.session_state

        if has_chat_bot and not st.session_state.get("conversation_processed", False):
            with st.spinner("Extracting candidate data..."):
                st.session_state.chat_bot.process_conversation()  # Uses SUMMARY_MODEL
            progress_bar.progress(100)
            st.success("✅ Data processed and saved to database!")
            st.session_state.conversation_processed = True

        elif st.session_state.get("conversation_processed", False):
            progress_bar.progress(100)
            st.success("✅ Data already processed.")

        else:
            # No chat data found — give user a way out
            st.warning("⚠️ No chat data found. Nothing to process.")

        # Always show the Back to Home button so the user is never stuck
        if st.button("🏠 Back to Home", use_container_width=True):
            for key in ["chat_messages", "chat_bot", "conversation_processed"]:
                st.session_state.pop(key, None)
            st.session_state.current_screen = "home"
            st.rerun()
