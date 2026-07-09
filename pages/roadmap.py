import streamlit as st
from components.sidebar import show_sidebar
from tools.gemini_client import ask_gemini

st.set_page_config(
    page_title="Learning Roadmap",
    page_icon="🗺",
    layout="wide",
)
st.session_state["current_page"] = "roadmap"
show_sidebar()

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f6ebff 0%, #e9dcff 55%, #efe6ff 100%) !important;
    }
    section[data-testid="main"] {
        background: transparent;
    }
    div.block-container {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(109, 74, 255, 0.16);
        border-radius: 24px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 12px 30px rgba(80, 54, 170, 0.12);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #184a8f 0%, #4b7fe8 100%) !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .profile-name,
    section[data-testid="stSidebar"] .profile-email,
    section[data-testid="stSidebar"] .sidebar-header h2,
    section[data-testid="stSidebar"] .sidebar-header p,
    section[data-testid="stSidebar"] .sidebar-quote h4,
    section[data-testid="stSidebar"] .sidebar-quote p,
    section[data-testid="stSidebar"] .sidebar-quote small {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.16) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.24) !important;
        border-radius: 999px !important;
    }

    div[data-testid="stVerticalBlock"] > div > label,
    div[data-testid="stVerticalBlock"] > div > div > label,
    .stTextInput label,
    .stButton > button,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown p {
        color: #5b21b6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<h1 style='font-size:55px;font-weight:800;color:#6C63FF;'>
🗺 Learning Roadmap
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='color:#4b5563;'>
Build a structured roadmap for any skill with AI guidance.
</h4>
""", unsafe_allow_html=True)

st.write("")

skill = st.text_input("Enter a skill", placeholder="Example: Python")

if st.button("Generate Roadmap", use_container_width=True):
    prompt = f"""
    Create a complete learning roadmap for {skill}.

    Include:
    - Beginner
    - Intermediate
    - Advanced
    - Projects
    - Certifications
    """

    response = ask_gemini(prompt)
    st.markdown(
        """
        <style>
        .roadmap-result-box {
            background: #ffffff !important;
            border: 1px solid rgba(109, 74, 255, 0.16) !important;
            border-radius: 18px !important;
            padding: 1rem 1.15rem !important;
            box-shadow: 0 8px 22px rgba(80, 54, 170, 0.08) !important;
            margin-top: 0.75rem !important;
            color: #111827 !important;
            line-height: 1.7 !important;
        }
        .roadmap-result-box p,
        .roadmap-result-box li,
        .roadmap-result-box strong,
        .roadmap-result-box em,
        .roadmap-result-box span,
        .roadmap-result-box div {
            color: #111827 !important;
        }
        .roadmap-result-box h1,
        .roadmap-result-box h2,
        .roadmap-result-box h3,
        .roadmap-result-box h4,
        .roadmap-result-box h5,
        .roadmap-result-box h6 {
            color: #312e81 !important;
            margin-top: 0.6rem !important;
            margin-bottom: 0.35rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='roadmap-result-box'>{response}</div>", unsafe_allow_html=True)