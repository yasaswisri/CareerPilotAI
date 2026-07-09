import streamlit as st

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀"
)

if "code" in st.query_params or "error" in st.query_params:
    st.session_state["google_oauth_callback"] = dict(st.query_params)
    try:
        st.switch_page("pages/login.py")
    except Exception:
        st.switch_page("pages/login.py")
else:
    st.switch_page("pages/signup.py")