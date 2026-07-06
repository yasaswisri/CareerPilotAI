import streamlit as st
from components.sidebar import show_sidebar

st.set_page_config(page_title="Saved", layout="wide")

show_sidebar()

st.title("🔖 Saved")

st.info("Your saved resumes, roadmaps and interview sessions will appear here.")