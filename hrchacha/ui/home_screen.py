import streamlit as st


class HomeScreen:
    def __init__(self):
        self.title = "HRchacha - AI Hiring Assistant by TalentScout"
        st.set_page_config(
            page_title=self.title,
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def render(self):
        st.markdown(
            """
            <div style="text-align:center; margin-top:3rem;">
                <h1 style="font-size:3rem;">HRChacha</h1>
                <p style="color:#94a3b8; font-size:1.1rem;">
                    AI Hiring Assistant by <b>TalentScout</b><br>
                    Dual-LLM pipeline: Live interviewing + secure post-chat summarization
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                """
                <div style="
                    background: linear-gradient(135deg, #020617, #020617);
                    padding: 1.5rem;
                    border-radius: 16px;
                    border: 1px solid #1e293b;
                ">
                    <h3>Why HRChacha?</h3>
                    <ul style="color:#cbd5f5;">
                        <li>⚡ Intelligent candidate screening</li>
                        <li>🎯 Structured AI interviews</li>
                        <li>🧾 Automatic JSON summaries saved to MongoDB</li>
                        <li>🔐 No data stored until you end the chat</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 Start Chat", use_container_width=True):
                st.session_state.current_screen = "chat"
                st.rerun()

        st.markdown(
            "<p style='text-align:center; color:#64748b; margin-top:3rem;'>"
            "© TalentScout · HRChacha AI</p>",
            unsafe_allow_html=True
        )
