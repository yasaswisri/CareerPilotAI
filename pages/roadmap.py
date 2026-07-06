import streamlit as st
from tools.gemini_client import ask_gemini

st.title("🗺 Learning Roadmap")

skill = st.text_input("Enter a skill")

if st.button("Generate Roadmap"):
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
    st.write(response)