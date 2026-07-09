import streamlit as st
from auth import clear_session, get_user_profile, load_session, update_user_profile
from components.sidebar import show_sidebar
from components.theme import apply_theme_css, sync_user_context

st.set_page_config(page_title="Profile", layout="wide")
sync_user_context()
apply_theme_css()
st.session_state["current_page"] = "profile"
show_sidebar()

st.markdown(
    """
    <style>
    .page-title { font-size: 2.2rem; font-weight: 800; color: var(--text) !important; margin-bottom: 0.2rem; }
    .page-subtitle { color: var(--muted) !important; margin-bottom: 1rem; }
    .card { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 18px; padding: 1rem 1.1rem; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); margin-bottom: 1rem; }
    .card h3 { color: var(--text) !important; margin-top: 0; }
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stRadio"] label,
    .stMarkdown p,
    .stMarkdown strong {
        color: var(--text) !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div {
        color: var(--text) !important;
        background: var(--surface-2) !important;
    }
    div[data-testid="stTextInput"] input:disabled,
    div[data-testid="stTextArea"] textarea:disabled,
    div[data-testid="stNumberInput"] input:disabled {
        color: var(--text) !important;
        background: var(--surface-2) !important;
        opacity: 1 !important;
        -webkit-text-fill-color: var(--text) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='page-title'>👤 Profile</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Manage your profile details and keep your account information up to date.</div>", unsafe_allow_html=True)

session_user = load_session() or {}
current_email = st.session_state.get("email") or session_user.get("email")
if not current_email:
    st.warning("Please sign in to view your profile.")
    st.stop()

profile_data = get_user_profile(current_email) or {}
profile_picture = profile_data.get("profile_picture") or st.session_state.get("profile_picture")
full_name = profile_data.get("name") or st.session_state.get("name", "Guest")
email = profile_data.get("email") or current_email
phone = profile_data.get("phone", "")
college = profile_data.get("education", "")
skills = profile_data.get("skills", "")
resume_score = profile_data.get("resume_score", 0)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Profile Overview</h3>", unsafe_allow_html=True)

col_a, col_b = st.columns([0.9, 2.1], gap="large")
with col_a:
    if profile_picture:
        st.image(profile_picture, width=180)
    else:
        initials = (full_name or "U")[0].upper()
        st.markdown(f"<div style='width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #6d4aff, #4f46e5); color: white; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: 700;'> {initials}</div>", unsafe_allow_html=True)
with col_b:
    full_name_input = st.text_input("Full Name", value=full_name, key="profile_full_name")
    email_input = st.text_input("Email", value=email, disabled=True)
    phone_input = st.text_input("Phone Number", value=phone, placeholder="Add your phone number", key="profile_phone")
    college_input = st.text_input("College", value=college, placeholder="Your college or university", key="profile_college")
    skills_input = st.text_area("Skills", value=skills, placeholder="Add your top skills", key="profile_skills")
    resume_score_input = st.number_input("Resume Score", min_value=0, max_value=100, value=int(resume_score or 0), key="profile_resume_score")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    if st.button("Save Changes", use_container_width=True):
        payload = {
            "name": full_name_input,
            "phone": phone_input,
            "education": college_input,
            "skills": skills_input,
            "resume_score": int(resume_score_input),
        }
        if update_user_profile(current_email, payload):
            st.session_state["name"] = full_name_input
            st.success("Profile updated successfully.")
        else:
            st.error("Unable to update your profile right now.")
with col2:
    if st.button("Logout", use_container_width=True):
        clear_session()
        for key in list(st.session_state.keys()):
            if key != "current_page":
                st.session_state.pop(key, None)
        st.session_state["current_page"] = "login"
        st.session_state["authenticated"] = False
        st.session_state["name"] = "Guest"
        st.session_state["email"] = "guest@example.com"
        st.switch_page("pages/login.py")