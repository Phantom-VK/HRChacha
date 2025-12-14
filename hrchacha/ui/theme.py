import streamlit as st

def apply_dark_blue_theme():
    st.markdown(
        """
        <style>
        /* ===== App Background ===== */
        .stApp {
            background: radial-gradient(
                circle at top,
                #0f172a 0%,
                #020617 45%,
                #000000 100%
            );
            color: #e5e7eb;
            font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont;
        }

        /* ===== Remove Streamlit Chrome ===== */
        #MainMenu, footer, header {
            visibility: hidden;
        }

        /* ===== Titles ===== */
        h1, h2, h3 {
            color: #e5e7eb;
            letter-spacing: -0.5px;
        }

        /* ===== Buttons ===== */
        .stButton > button {
            background: linear-gradient(135deg, #2563eb, #1e40af);
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            border: none;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35);
        }

        /* ===== Chat Container ===== */
        .stChatMessage {
            border-radius: 14px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.6rem;
            animation: fadeIn 0.25s ease-in;
        }

        /* User Message */
        .stChatMessage[data-testid="stChatMessage"][aria-label="user"] {
            background: linear-gradient(135deg, #1e293b, #020617);
            border-left: 3px solid #3b82f6;
        }

        /* Bot Message */
        .stChatMessage[data-testid="stChatMessage"][aria-label="assistant"] {
            background: linear-gradient(135deg, #020617, #020617);
            border-left: 3px solid #22d3ee;
        }

        /* Chat Input */
        .stChatInput textarea {
            background-color: #020617;
            color: #e5e7eb;
            border-radius: 12px;
            border: 1px solid #1e293b;
        }

        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #2563eb, #22d3ee);
        }

        /* Subtle animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
