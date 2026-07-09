import streamlit as st
from PyPDF2 import PdfReader
from tools.gemini_client import ask_gemini
from prompts.resume_prompt import RESUME_PROMPT
from components.sidebar import show_sidebar

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.session_state["current_page"] = "resume"
show_sidebar()

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    st.success("Resume uploaded successfully!")

    st.subheader("Extracted Resume")
    st.text_area("", text, height=250)

    if st.button("Analyze Resume with AI"):
        with st.spinner("Analyzing your resume..."):

            prompt = RESUME_PROMPT.replace("{text}", text)

            result = ask_gemini(prompt)

            st.subheader("AI Resume Analysis")
            st.markdown(result)
        st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
header{
    visibility:hidden;
}
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}

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

.stTitle, .stSubheader, .stMarkdown, .stFileUploader label, .stTextArea textarea {
    color: #1f2937 !important;
}

.stTextArea textarea, .stTextInput input {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #cdbdff !important;
    border-radius: 12px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6d4aff, #4f46e5) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.45rem 1.1rem !important;
}

.stSuccess {
    background: rgba(76, 175, 80, 0.12) !important;
    color: #1a5f2d !important;
    border: 1px solid rgba(76, 175, 80, 0.25) !important;
    border-radius: 10px !important;
}
.st-emotion-cache-13k62yr {
    position: absolute;
    background: rgb(14, 17, 23);
    color: rgb(28, 131, 225);
    inset: 0px;
    color-scheme: dark;
    overflow: hidden;
}
            </style>
""", unsafe_allow_html=True)
