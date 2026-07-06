import streamlit as st
from tools.gemini_client import ask_gemini

st.title("🎤 Interview Coach")

role = st.text_input("Enter Job Role")

if st.button("Generate Interview Questions"):
    prompt = f"""
    Generate 10 interview questions for a {role}.

    Also provide sample answers.
    """

    response = ask_gemini(prompt)
    st.write(response)