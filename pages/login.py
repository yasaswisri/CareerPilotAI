import re
import time
import streamlit as st
from auth import clear_session, load_session, login, save_session
st.markdown(
    '<div class="login-page">',
    unsafe_allow_html=True
)
# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- HIDE STREAMLIT DEFAULT UI ----------------

hide_streamlit = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container{
    padding-top:0rem;
    padding-bottom:0rem;
    padding-left:0rem;
    padding-right:0rem;
}
</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)

# ---------------- LOAD CSS ----------------

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific UI tweaks (animations, button styles, link underline)
st.markdown(
    """
    <style>
    /* Scope styles to the right panel */
    .login-right .stButton>button {
        background: linear-gradient(90deg,#6C63FF,#3B82F6) !important;
        color: purple !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        transition: transform .3s ease, box-shadow .3s ease, filter .1s ease !important;
        box-shadow: none !important;
        cursor: pointer !important;
        border: none !important;
    }

    .login-right .stButton>button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 10px 30px rgba(60,99,255,0.18) !important;
    }

    .login-right .stButton>button:active {
        filter: brightness(.92) !important;
    }

    /* Scoped links (Forgot Password, Sign Up) inside right panel */
    .login-right a {
        color: #3B82F6 !important;
        text-decoration: none !important;
        position: relative !important;
        transition: color .3s ease !important;
        font-weight: 600 !important;
        cursor: pointer !important;
    }

    .login-right a::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: -2px;
        height: 2px;
        width: 100%;
        background: linear-gradient(90deg,#6C63FF,#3B82F6);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform .3s ease;
        opacity: 0.95;
    }

    .login-right a:hover { color: #2563EB !important; }
    .login-right a:hover::after { transform: scaleX(1); }

    /* Responsive tweaks */
    @media (max-width: 900px) {
        .login-right .stButton>button { padding: 10px 14px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

saved_session = load_session()
if saved_session:
    st.session_state["authenticated"] = True
    st.session_state["name"] = saved_session.get("name", "Guest")
    st.session_state["email"] = saved_session.get("email", "")
    st.session_state["remember_me"] = saved_session.get("remember_me", False)
    st.switch_page("pages/home.py")

# ---------------- PAGE LAYOUT ----------------

left, right = st.columns([3, 2], gap="large")

# ======================================================
# LEFT PANEL
# ======================================================

with left:
    st.html("""
    <div class="login-left">
        <div class="glass-card">
            <div class="hero-content">

                <div class="hero-logo">
                    🚀 <span>CareerPilot AI</span>
                </div>

                <h1 class="welcome">Welcome to <span>CareerPilot AI</span></h1>

                <p class="lead">
                    Your AI-powered companion for career guidance,
                    resume building, interview preparation and job opportunities.
                </p>

            </div>
        </div>
    </div>
    """)

# ======================================================
# RIGHT PANEL
# ======================================================

with right:
    st.markdown('<div class="login-right"><div class="login-card">', unsafe_allow_html=True)

    st.markdown(
        "<h1 class='brand-title'>CareerPilot <span>AI</span></h1>",
        unsafe_allow_html=True,
    )

    st.markdown("<h2 class=\"login-heading\">Login</h2>", unsafe_allow_html=True)

    st.markdown(
        "<p class='subtitle'>Continue your journey towards success</p>",
        unsafe_allow_html=True,
    )

    st.session_state.setdefault("login_attempted", False)
    st.session_state.setdefault("email_error", "")
    st.session_state.setdefault("password_error", "")
    st.session_state.setdefault("auth_error", "")

    email_value = st.session_state.get("login_email", "")
    password_value = st.session_state.get("login_password", "")

    if st.session_state["login_attempted"]:
        if not email_value.strip():
            st.session_state["email_error"] = "Please enter your email."
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_value.strip()):
            st.session_state["email_error"] = "Please enter a valid email address."
        else:
            st.session_state["email_error"] = ""

        if not password_value.strip():
            st.session_state["password_error"] = "Please enter your password."
        else:
            st.session_state["password_error"] = ""

    email = st.text_input(
        "Email",
        value=st.session_state.get("remembered_email", ""),
        key="login_email",
        placeholder="Enter your email",
    )

    if st.session_state["email_error"]:
        st.error(st.session_state["email_error"])

    password = st.text_input(
        "Password",
        type="password",
        key="login_password",
        placeholder="Enter your password",
    )

    if st.session_state["password_error"]:
        st.error(st.session_state["password_error"])

    if st.session_state["auth_error"]:
        st.error(st.session_state["auth_error"])

    # Forgot Password
    fp1, fp2 = st.columns([3, 1])
    with fp2:
        st.page_link("pages/forgot_password.py", label="Forgot Password?")

    # Login Button
    login_btn = st.button("Login", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
<style>
.signup-row{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:6px;
    margin-top:15px;
    font-size:15px;
    color:#666;
}

.signup-row a{
    color:#6C63FF;
    font-weight:600;
    text-decoration:none;
    transition:.3s;
}

.signup-row a:hover{
    color:#3B82F6;
    text-decoration:underline;
}
</style>

<div class="signup-row">
    <span>Don't have an account?</span>
    <a href="/signup" target="_self" class="signup-link">Sign Up</a>
</div>
""", unsafe_allow_html=True)
    # close markup wrappers opened above
    st.markdown('</div></div>', unsafe_allow_html=True)
# ======================================================
# LOGIN LOGIC
# ======================================================

if login_btn:
    st.session_state["login_attempted"] = True
    st.session_state["auth_error"] = ""

    email_value = st.session_state.get("login_email", "")
    password_value = st.session_state.get("login_password", "")

    st.session_state["email_error"] = ""
    st.session_state["password_error"] = ""

    if not email_value.strip():
        st.session_state["email_error"] = "Please enter your email."
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_value.strip()):
        st.session_state["email_error"] = "Please enter a valid email address."

    if not password_value.strip():
        st.session_state["password_error"] = "Please enter your password."

    if st.session_state["email_error"] or st.session_state["password_error"]:
        st.rerun()

    user = login(email_value.strip().lower(), password_value)

    if user:
        st.session_state["name"] = user[1]
        st.session_state["email"] = user[2]
        st.session_state["authenticated"] = True
        st.success("Login Successful! Redirecting...")
        time.sleep(1)
        st.switch_page("pages/home.py")
    else:
        st.session_state["auth_error"] = "Invalid email or password."
        st.rerun()
        