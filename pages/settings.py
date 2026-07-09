import json
import streamlit as st

from auth import clear_session, delete_user_account, get_user_profile, load_session, update_user_settings
from components.sidebar import show_sidebar
from components.theme import apply_theme_css, sync_user_context

st.set_page_config(page_title="Settings", layout="wide")
sync_user_context()
apply_theme_css()
st.session_state["current_page"] = "settings"
show_sidebar()

st.markdown(
    """
    <style>
    .page-title { font-size: 2.2rem; font-weight: 800; color: var(--text) !important; margin-bottom: 0.2rem; }
    .page-subtitle { color: var(--muted) !important; margin-bottom: 1rem; }
    .card { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 18px; padding: 1rem 1.1rem; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); margin-bottom: 1rem; }
    .card h3 { color: var(--text) !important; margin-top: 0; }
    .stApp, .stApp * {
        color: var(--text) !important;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stSelectbox"] label,
    .stMarkdown p,
    .stMarkdown strong,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] strong {
        color: var(--text) !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div,
    div[data-testid="stRadio"] div,
    div[data-testid="stCheckbox"] div {
        color: var(--text) !important;
        background: var(--surface-2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
        color: white !important;
        border: none !important;
        border-radius: 999px !important;
        box-shadow: 0 8px 24px rgba(80, 54, 170, 0.16) !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        filter: brightness(1.04) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(109, 74, 255, 0.18) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='page-title'>⚙ Settings</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Adjust your experience, notifications, privacy, and account preferences.</div>", unsafe_allow_html=True)

session_user = load_session() or {}
current_email = st.session_state.get("email") or session_user.get("email")
if not current_email:
    st.warning("Please sign in before adjusting your settings.")
    st.stop()

profile_data = get_user_profile(current_email) or {}
settings_defaults = {
    "theme_mode": profile_data.get("theme_mode") or ("dark" if profile_data.get("dark_mode", 0) else "light"),
    "language": profile_data.get("language") or "English",
    "response_style": profile_data.get("response_style") or "Balanced",
    "email_notifications": bool(profile_data.get("email_notifications", 1)),
    "push_notifications": bool(profile_data.get("push_notifications", 1)),
    "share_anonymous_usage_data": bool(profile_data.get("share_anonymous_usage_data", 0)),
}
for key, value in settings_defaults.items():
    st.session_state.setdefault(key, value)


def selected_index(options, value):
    try:
        return options.index(value)
    except ValueError:
        return 0

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Appearance</h3>", unsafe_allow_html=True)
theme_options = ["Light", "Dark", "System"]
theme_label = {"light": "Light", "dark": "Dark", "system": "System"}.get(st.session_state.get("theme_mode", "light"), "Light")
theme_choice = st.radio("Theme Mode", theme_options, index=selected_index(theme_options, theme_label), key="theme_choice")
selected_theme_mode = theme_choice.lower()
if st.session_state.get("theme_mode") != selected_theme_mode:
    st.session_state["theme_mode"] = selected_theme_mode
    apply_theme_css()
language = st.selectbox("Language", ["English", "Hindi", "Spanish"], index=selected_index(["English", "Hindi", "Spanish"], st.session_state.get("language", "English")), key="language")
response_style = st.selectbox("AI response style", ["Concise", "Detailed", "Balanced"], index=selected_index(["Concise", "Detailed", "Balanced"], st.session_state.get("response_style", "Balanced")), key="response_style")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Notifications</h3>", unsafe_allow_html=True)
email_notifications = st.checkbox("Email notifications", value=st.session_state.get("email_notifications", True), key="email_notifications")
push_notifications = st.checkbox("Push notifications", value=st.session_state.get("push_notifications", True), key="push_notifications")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Account</h3>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    if st.button("Change Password", use_container_width=True):
        st.switch_page("pages/forgot_password.py")
with col_b:
    if st.button("Update Profile", use_container_width=True):
        st.switch_page("pages/profile.py")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Privacy</h3>", unsafe_allow_html=True)
share_anonymous_usage_data = st.checkbox("Data privacy", value=st.session_state.get("share_anonymous_usage_data", False), key="share_anonymous_usage_data")
if st.button("Delete Account", use_container_width=True):
    if delete_user_account(current_email):
        clear_session()
        for key in list(st.session_state.keys()):
            if key != "current_page":
                st.session_state.pop(key, None)
        st.session_state["current_page"] = "login"
        st.success("Account deleted successfully.")
        st.stop()
    st.error("Unable to delete the account right now.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>About</h3>", unsafe_allow_html=True)
st.markdown("**Version:** 1.0.0")
st.markdown("**Terms & Privacy Policy:** Our policies are available in Help & Support.")
if st.button("Open Help & Support", use_container_width=True):
    st.switch_page("pages/support.py")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Save Preferences", use_container_width=True):
    payload = {
        "theme_mode": theme_choice.lower(),
        "language": language,
        "response_style": response_style,
        "email_notifications": int(email_notifications),
        "push_notifications": int(push_notifications),
        "share_anonymous_usage_data": int(share_anonymous_usage_data),
    }
    if update_user_settings(current_email, payload):
        st.session_state["theme_mode"] = theme_choice.lower()
        apply_theme_css()
        st.success("Preferences saved successfully.")
        st.rerun()
    else:
        st.error("Unable to save settings right now.")

