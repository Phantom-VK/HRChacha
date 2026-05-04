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

    def _initialize_app_state(self):
        """Initialize the main app state."""
        if "current_screen" not in st.session_state:
            st.session_state.current_screen = "home"
        if "conversation_processed" not in st.session_state:
            st.session_state.conversation_processed = False
        if "processing_status" not in st.session_state:
            st.session_state.processing_status = "not_started"

    def run(self):
        """Main app runner — handles screen navigation."""
        screen = st.session_state.current_screen

        if screen == "home":
            self.home_screen.render()
        elif screen == "chat":
            ChatUI("HRChacha - TalentScout").render()
        elif screen == "processing":
            self._show_processing_screen()

    @staticmethod
    def _reset_session_to_home():
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

    def _show_processing_screen(self):
        """Process conversation with Summary LLM and save to DB."""
        st.title("⏳ Processing Your Session")
        st.markdown("**HRChacha is extracting your data...**")

        if st.button("🏠 Back to Home", use_container_width=True):
            self._reset_session_to_home()

        progress_bar = st.progress(0)

        has_chat_bot = "chat_bot" in st.session_state
        processing_status = st.session_state.get("processing_status", "not_started")

        if has_chat_bot and processing_status == "not_started":
            with st.spinner("Extracting candidate data..."):
                st.session_state.processing_status = "processing"
                processed = st.session_state.chat_bot.process_conversation()  # Uses SUMMARY_MODEL
            if processed:
                progress_bar.progress(100)
                st.session_state.conversation_processed = True
                st.session_state.processing_status = "succeeded"
            else:
                progress_bar.progress(0)
                st.session_state.processing_status = "failed"

        elif processing_status == "succeeded" or st.session_state.get("conversation_processed", False):
            progress_bar.progress(100)
            st.success("✅ Data already processed.")

        elif processing_status == "failed":
            progress_bar.progress(0)
            st.error("Processing failed. Check logs for the extraction or MongoDB upload failure.")
            if st.button("Retry Processing", use_container_width=True):
                st.session_state.processing_status = "not_started"
                st.session_state.conversation_processed = False
                st.rerun()

        elif processing_status == "processing":
            st.info("Processing is already in progress. Please wait.")

        else:
            # No chat data found — give user a way out
            st.warning("⚠️ No chat data found. Nothing to process.")
