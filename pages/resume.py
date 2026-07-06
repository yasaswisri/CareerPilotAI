import streamlit as st
from PyPDF2 import PdfReader
from tools.gemini_client import ask_gemini
from prompts.resume_prompt import RESUME_PROMPT

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")

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
[data-testid="stSidebar"]{
    display:none;
}
[data-testid="collapsedControl"]{
    display:none;
}
[data-testid="stSidebarNav"]{
    display:none;
}
#MainMenu{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
header{
    visibility:hidden;
}
</style>
""", unsafe_allow_html=True)