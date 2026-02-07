import streamlit as st

from hrchacha.ui.chat_ui import ChatUI
from hrchacha.ui.home_screen import HomeScreen
from hrchacha.ui.theme import apply_dark_blue_theme


class MainWindowUI:
    def __init__(self):
        apply_dark_blue_theme()
        self.home_screen = HomeScreen()
        self.chat_ui = ChatUI("HRChacha - TalentScout")
        self._initialize_app_state()

    def _initialize_app_state(self):
        """Initialize the main app state."""
        if "current_screen" not in st.session_state:
            st.session_state.current_screen = "home"
        if "conversation_processed" not in st.session_state:
            st.session_state.conversation_processed = False

    def run(self):
        """Main app runner - handles screen navigation."""
        if st.session_state.current_screen == "home":
            self.home_screen.render()

        elif st.session_state.current_screen == "chat":
            self.chat_ui.render()

        elif st.session_state.current_screen == "processing":
            self._show_processing_screen()

    def _show_processing_screen(self):
        """Process conversation with Summary LLM and save to DB."""
        st.title("⏳ Processing Your Session")
        st.markdown("**HRChacha is extracting your data...**")

        progress_bar = st.progress(0)

        # Process with Summary LLM
        if "chat_bot" in st.session_state and not st.session_state.get("conversation_processed", False):
            with st.spinner(text="Extracting candidate data..."):
                st.session_state.chat_bot.process_conversation()  # Uses SUMMARY_MODEL

            progress_bar.progress(100)
            st.success("✅ Data processed and saved to database!")
            st.session_state.conversation_processed = True
        elif st.session_state.get("conversation_processed", False):
            progress_bar.progress(100)
            st.success("✅ Data already processed.")

        if st.button("🏠 Back to Home", use_container_width=True):
            # Reset chat state
            for key in ["chat_messages", "chat_bot", "conversation_processed", "last_processed_email"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_screen = "home"
            st.rerun()
        else:
            st.warning("No chat data found.")
