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

    def run(self):
        """Main app runner - handles screen navigation."""
        if st.session_state.current_screen == "home":
            self.home_screen.render()

        elif st.session_state.current_screen == "chat":
            self.chat_ui.render()

        elif st.session_state.current_screen == "processing":
            self._show_processing_screen()

    def _show_processing_screen(self):
        """Shows post-chat processing screen."""
        st.set_page_config(page_title="Processing...", page_icon="⏳")

        st.title("⏳ Processing Your Session")
        st.markdown(
            "<p style='color:#94a3b8;'>Please wait while we finalize insights.</p>",
            unsafe_allow_html=True
        )

        progress_bar = st.progress(0)
        status_text = st.empty()

        # Simulate processing (replace with actual processing logic)
        import time
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Processing... {i + 1}%")
            time.sleep(0.03)

        st.success("✅ Session processed successfully!")
        st.balloons()

        if st.button("🏠 Back to Home", use_container_width=True):
            # Reset chat state
            if "chat_messages" in st.session_state:
                del st.session_state.chat_messages
            if "chat_bot" in st.session_state:
                del st.session_state.chat_bot
            st.session_state.current_screen = "home"
            st.rerun()
