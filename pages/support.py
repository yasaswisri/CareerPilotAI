import streamlit as st
from auth import clear_session, load_session
from components.sidebar import show_sidebar
from components.theme import apply_theme_css, sync_user_context

st.set_page_config(page_title="Help & Support", layout="wide")
sync_user_context()
apply_theme_css()
st.session_state["current_page"] = "support"
show_sidebar()

st.markdown("<div class='page-title'>❓ Help & Support</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Get help, share feedback, or report an issue with CareerPilot AI.</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>FAQ</h3>", unsafe_allow_html=True)
st.markdown("- How do I update my profile? Open the Profile page from the sidebar or dropdown.")
st.markdown("- How do I change the app theme? Use the Settings page or the Theme option in the profile menu.")
st.markdown("- How do I contact support? Use the contact form below or email support@careerpilotai.com.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Contact Support</h3>", unsafe_allow_html=True)
st.markdown("Email: support@careerpilotai.com")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Feedback</h3>", unsafe_allow_html=True)
subject = st.text_input("Subject", placeholder="Briefly describe your issue")
message = st.text_area("Message", placeholder="Share details about the problem or feature request")
if st.button("Submit", use_container_width=True):
    if subject and message:
        st.success("Thank you for your feedback. Our team will review it shortly.")
    else:
        st.warning("Please provide both a subject and a message.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>About CareerPilot AI</h3>", unsafe_allow_html=True)
st.markdown("CareerPilot AI helps users build stronger resumes, practice interviews, and plan their career growth using intelligent guidance.")
st.markdown("</div>", unsafe_allow_html=True)
