import random
from pathlib import Path

from PIL import Image
import streamlit as st
from auth import clear_session, load_session, update_user_settings
from tools.gemini_client import ask_gemini
from components.sidebar import show_sidebar
from components.theme import apply_theme_css, get_display_user_info, sync_user_context

sync_user_context()
session_data = load_session()
if not session_data and not st.session_state.get("authenticated"):
    st.switch_page("pages/login.py")


def render_hero_visual():
    """Render the hero image using the first valid image asset available."""
    candidates = ["assets/background.jpg", "assets/avatar.png"]

    for image_path in candidates:
        file_path = Path(image_path)
        if not file_path.exists():
            continue

        try:
            with Image.open(file_path) as img:
                img.verify()
            st.image(image_path, use_container_width=True)
            return
        except Exception:
            continue

    st.markdown(
        """
        <div class='hero-visual' style='min-height: 280px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #6C63FF, #4F8EF7); color: white; font-size: 1.3rem; font-weight: 600; text-align: center;'>
            CareerPilot AI
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="wide")

# ---------------- LOAD CSS ----------------
with open("assets/style.css", encoding="utf-8") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
apply_theme_css()

# ---------------- SIDEBAR ----------------
st.session_state["current_page"] = "home"
show_sidebar()

# ---------------- TOP TOOLBAR ----------------
name, email, profile_picture = get_display_user_info()

st.markdown("<div class='hero-page-shell'>", unsafe_allow_html=True)

toolbar_left, toolbar_right = st.columns([3.2, 1.4], gap="small")
with toolbar_left:
    st.markdown(
        """
        <div class='hero-brand'>
            <div class='hero-brand-icon'>✦</div>
            <div>
                <div class='hero-brand-title'>CareerPilot AI</div>
                <div class='hero-brand-subtitle'>AI career platform</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with toolbar_right:
    theme_mode = st.session_state.get("theme_mode", "light")
    control_cols = st.columns([1, 1, 1.4], gap="small")
    with control_cols[0]:
        if st.button("☀️" if theme_mode == "dark" else "🌙", key="theme_toggle", help="Toggle theme", use_container_width=True):
            st.session_state["theme_mode"] = "dark" if theme_mode == "light" else "light"
    with control_cols[1]:
        if st.button("🔔", key="notifications", help="Notifications", use_container_width=True):
            st.session_state["toast"] = "You're all caught up for now."
    with control_cols[2]:
        with st.popover("👤"):
            theme_mode = st.session_state.get("theme_mode", "light")
            shell_class = "profile-menu-shell dark" if theme_mode == "dark" else "profile-menu-shell"
            avatar_html = f"<div class='profile-menu-avatar'>{name[0].upper() if name else 'U'}</div>"
            if profile_picture:
                avatar_html = f"<img class='profile-menu-photo' src='{profile_picture}' alt='avatar' />"
            st.markdown(
                f"""
                <div class="{shell_class}">
                    <div class="profile-menu-header">
                        {avatar_html}
                        <div>
                            <div class="profile-menu-name">{name}</div>
                            <div class="profile-menu-email">{email}</div>
                            <div class="profile-menu-status"><span></span>Online</div>
                        </div>
                    </div>
                    <div class="profile-menu-divider"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("👤 My Profile", key="profile_menu", use_container_width=True):
                st.switch_page("pages/profile.py")
            if st.button("⚙ Settings", key="settings_menu", use_container_width=True):
                st.switch_page("pages/settings.py")
            theme_options = ["Light", "Dark", "System"]
            theme_index = 0
            theme_label = {"light": "Light", "dark": "Dark", "system": "System"}.get(theme_mode, "Light")
            if theme_label in theme_options:
                theme_index = theme_options.index(theme_label)
            selected_theme = st.radio("Theme", theme_options, index=theme_index, key="dropdown_theme_mode", horizontal=False)
            if st.button("Apply Theme", key="apply_theme_menu", use_container_width=True):
                new_mode = selected_theme.lower()
                st.session_state["theme_mode"] = new_mode
                if st.session_state.get("authenticated") and st.session_state.get("email"):
                    update_user_settings(st.session_state["email"], {"theme_mode": new_mode})
                st.rerun()
            if st.button("❓ Help & Support", key="help_menu", use_container_width=True):
                st.switch_page("pages/support.py")
            st.markdown("<div class='profile-menu-divider'></div>", unsafe_allow_html=True)
            if st.session_state.get("confirm_logout"):
                st.warning("Are you sure you want to log out?")
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("Yes, logout", key="confirm_logout_yes", use_container_width=True):
                        clear_session()
                        for key in list(st.session_state.keys()):
                            if key != "current_page":
                                st.session_state.pop(key, None)
                        st.session_state["current_page"] = "login"
                        st.session_state["authenticated"] = False
                        st.session_state["name"] = "Guest"
                        st.session_state["email"] = "guest@example.com"
                        st.switch_page("pages/login.py")
                with col_cancel:
                    if st.button("Cancel", key="confirm_logout_cancel", use_container_width=True):
                        st.session_state["confirm_logout"] = False
                        st.rerun()
            elif st.button("🚪 Logout", key="logout_menu", use_container_width=True):
                st.session_state["confirm_logout"] = True
                st.rerun()

if "toast" in st.session_state:
    st.success(st.session_state["toast"])

# ---------------- HERO SECTION ----------------
hero_left, hero_right = st.columns([1.7, 0.9], gap="medium")

with hero_left:
    st.markdown(
        """
        <div class="hero-shell">
            <div class="hero-badge">⚡ Powered by Gemini AI</div>
            <h1>Welcome to <span>CareerPilot AI</span></h1>
            <p class="hero-subtitle">Your premium AI career companion for resume growth, interview readiness, and smarter professional decisions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_cols = st.columns([5.6, 1.2], gap="small")
    with search_cols[0]:
        question = st.text_input(
            "",
            key="home_search",
            placeholder=f"Hi {name}! How can I help you today?",
            label_visibility="collapsed",
        )
    with search_cols[1]:
        if st.button("Send", key="home_search_button", use_container_width=True):
            if question:
                with st.spinner("Thinking..."):
                    answer = ask_gemini(question)
                st.session_state["home_answer"] = answer
            else:
                st.session_state["home_answer"] = "Please share what you want help with and I will guide you."

    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] {
            margin: 0 !important;
        }
        div[data-testid="stTextInput"] > div {
            height: 100% !important;
            min-height: 54px !important;
            display: flex !important;
            align-items: center !important;
        }
        div[data-testid="stTextInput"] input {
            height: 54px !important;
            min-height: 54px !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255,255,255,0.22) !important;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10) !important;
            padding: 0 16px !important;
            background: rgba(255,255,255,0.96) !important;
            font-size: 0.98rem !important;
            line-height: 54px !important;
        }
        div[data-testid="stButton"] {
            margin: 0 !important;
        }
        div[data-testid="stButton"] > button {
            height: 54px !important;
            min-height: 54px !important;
            border-radius: 14px !important;
            font-weight: 700 !important;
            padding: 0 18px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("home_answer"):
        st.markdown("### ✨ CareerPilot Insight")
        st.info(st.session_state["home_answer"])

with hero_right:
    st.markdown(
        """
        <div class="hero-dashboard-card">
            <div class="hero-dashboard-top">
                <div class="hero-avatar">AI</div>
                <div>
                    <div class="hero-dashboard-title">Welcome back</div>
                    <div class="hero-dashboard-name">{name}</div>
                </div>
            </div>
            <div class="hero-dashboard-stats">
                <div class="hero-stat-pill">
                    <div class="hero-stat-label">Resume Score</div>
                    <div class="hero-stat-value">92/100</div>
                </div>
                <div class="hero-stat-pill">
                    <div class="hero-stat-label">Learning Progress</div>
                    <div class="hero-stat-value">78%</div>
                </div>
            </div>
            <div class="hero-dashboard-footer">
                <div class="hero-tip-count">💡 12 Career Tips</div>
                <div class="hero-dashboard-action">
                    <a href="/resume" target="_self">Quick Action</a>
                </div>
            </div>
        </div>
        """.format(name=name),
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FEATURE CARDS ----------------

feature_cols = st.columns(4, gap="small")

feature_cards = [
    ("📄 Resume Analyzer", "resume", "Improve ATS score and polish your resume for the next opportunity.", "Open Resume", "pages/resume.py", "feature-card resume"),
    ("💼 Career Advisor", "career", "Get expert career guidance tailored to your goals and strengths.", "Get Advice", "pages/career.py", "feature-card career"),
    ("🎤 Interview Coach", "interview", "Practice mock interviews and sharpen your communication skills.", "Practice", "pages/interview.py", "feature-card interview"),
    ("🗺 Learning Roadmap", "roadmap", "Generate a step-by-step learning path aligned with your next milestone.", "Generate", "pages/roadmap.py", "feature-card roadmap"),
]

for index, (title, page_key, description, button_label, target, card_class) in enumerate(feature_cards):
    with feature_cols[index]:
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{description}</p>", unsafe_allow_html=True)
        if st.button(button_label, key=f"feature_{page_key}", use_container_width=True):
            st.switch_page(target)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- STATS ----------------
st.markdown("<h3 style='margin: 1.2rem 0 0.8rem; color: #20253a;'>CareerPilot Statistics</h3>", unsafe_allow_html=True)
stat_cols = st.columns(4, gap="small")
stat_data = [
    ("📄 Resumes Analyzed", "120+"),
    ("🎤 Interviews Practiced", "350+"),
    ("🧭 Career Paths", "75+"),
    ("🤖 AI Responses", "1000+"),
]
for idx, (label, value) in enumerate(stat_data):
    with stat_cols[idx]:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>{label}</div><div class='stat-value'>{value}</div></div>", unsafe_allow_html=True)

# ---------------- MOTIVATIONAL QUOTE ----------------
quotes = [
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("The future depends on what you do today.", "Mahatma Gandhi"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("Opportunities don't happen. You create them.", "Chris Grosser"),
    ("Hard work beats talent when talent doesn't work hard.", "Tim Notke"),
    ("The best way to predict the future is to create it.", "Peter Drucker"),
]
quote, author = random.choice(quotes)
st.markdown(f"""
<div class="quote-shell">
    <div style="font-size: 1.5rem; margin-bottom: 0.4rem;">❝</div>
    <h3>“{quote}”</h3>
    <p>— {author}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 1.25rem; color: #6b7280; text-align: center;'>© 2026 CareerPilot AI • Powered by Gemini AI</div>", unsafe_allow_html=True)