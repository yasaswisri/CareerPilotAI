import time
import streamlit as st
from auth import signup
st.markdown(
    '<div class="login-page">',
    unsafe_allow_html=True
)
st.set_page_config(
    page_title="CareerPilot AI - Sign Up",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CSS ----------------

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .signup-login-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        margin-top: 10px;
        margin-bottom: 2px;
        flex-wrap: wrap;
        width: 100%;
    }
    .signup-login-row a {
        color: #3B82F6 !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        transition: color 0.3s ease, text-decoration-color 0.3s ease !important;
        position: relative !important;
    }
    .signup-login-row a::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: -2px;
        width: 100%;
        height: 1.5px;
        background: linear-gradient(90deg, #6C63FF, #3B82F6);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    .signup-login-row a:hover {
        color: #2563EB !important;
    }
    .signup-login-row a:hover::after {
        transform: scaleX(1);
    }
    .signup-login-text {
        margin: 0;
        color: #6b7280;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- HEADER ----------------

st.markdown("<h1 class='page-title'>CareerPilot AI</h1>", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------

left, right = st.columns([1.1, 1])

# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.markdown("""
    <div class="left-panel">

    <div class="brand-logo">
    🚀
    </div>

    <h1>Your Career Begins Here</h1>

    <p class="subtitle">
    Build your future with AI-powered career guidance,
    resume analysis, interview preparation,
    and personalized learning.
    </p>

    <br>

    <div class="feature-box">
        🤖 AI Career Guidance
    </div>

    <div class="feature-box">
        📄 Resume Analyzer
    </div>

    <div class="feature-box">
        🎤 Interview Preparation
    </div>

    <div class="feature-box">
        🗺 Personalized Learning Roadmap
    </div>

    <br>

    <div class="quote-box">
    <h3>"Success doesn't come to you.
    You go to it."</h3>

    <p>— Marva Collins</p>
    </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    st.markdown("""
    <div class="signup-card">
    <h2>Create Your Account</h2>
    <p>Start your AI Career Journey today.</p>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create Password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm Password"
        )

        agree = st.checkbox(
            "I agree to the Terms & Conditions"
        )

        submit = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submit:
            pass

        st.markdown("""
<style>
.signup-login-row{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:6px;
    margin-top:18px;
    font-size:15px;
}

.signup-login-row span{
    color:#666666;
}

.signup-login-row a{
    color:#6C63FF;
    text-decoration:none;
    font-weight:600;
    position:relative;
    transition:all .3s ease;
}

.signup-login-row a::after{
    content:"";
    position:absolute;
    left:0;
    bottom:-2px;
    width:0%;
    height:2px;
    background:#6C63FF;
    transition:.3s;
}

.signup-login-row a:hover{
    color:#3B82F6;
}

.signup-login-row a:hover::after{
    width:100%;
}
</style>

<div class="signup-login-row">
    <span>Already have an account?</span>
    <a href="/login" target="_self">Login</a>
</div>
""", unsafe_allow_html=True)

    if submit:

        if name == "":
            st.warning("Enter your name")

        elif email == "":
            st.warning("Enter your email")

        elif len(password) < 8:
            st.warning("Password must contain at least 8 characters")

        elif password != confirm:
            st.error("Passwords do not match")

        elif not agree:
            st.warning("Accept Terms & Conditions")

        else:

            ok = signup(
                name.strip(),
                email.strip().lower(),
                password
            )

            if ok:
                st.success("Account created successfully!")
                st.markdown('<meta http-equiv="refresh" content="0; url=/login" />', unsafe_allow_html=True)
            else:

                st.error("Email already exists.")
                st.markdown("</div>", unsafe_allow_html=True)

