import streamlit as st
from components.sidebar import show_sidebar

st.set_page_config(page_title="History", layout="wide")

show_sidebar()

st.title("🕒 History")

st.info("Your AI conversations will appear here.")