import random
from pathlib import Path

from PIL import Image
import streamlit as st
from auth import load_session
from tools.gemini_client import ask_gemini
from components.sidebar import show_sidebar

session_data = load_session()
if not session_data and not st.session_state.get("authenticated"):
    st.switch_page("login.py")


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

# ---------------- SIDEBAR ----------------
st.session_state["current_page"] = "home"
show_sidebar()

# ---------------- TOP TOOLBAR ----------------
name = st.session_state.get("name", "Guest")

toolbar_cols = st.columns([4.5, 0.7, 0.7, 0.8])
with toolbar_cols[0]:
    st.markdown("<div class='page-kicker'>AI Career Platform</div>", unsafe_allow_html=True)

with toolbar_cols[1]:
    theme_mode = st.session_state.get("theme_mode", "light")
    if st.button("☀️" if theme_mode == "dark" else "🌙", key="theme_toggle", help="Toggle theme", use_container_width=True):
        st.session_state["theme_mode"] = "dark" if theme_mode == "light" else "light"

with toolbar_cols[2]:
    if st.button("🔔", key="notifications", help="Notifications", use_container_width=True):
        st.session_state["toast"] = "You're all caught up for now."

with toolbar_cols[3]:
    with st.popover("👤"):
        st.markdown(f"<div class='popover-card'><strong>{name}</strong><br/>{st.session_state.get('email', '')}</div>", unsafe_allow_html=True)
        if st.button("Profile", key="profile_menu", use_container_width=True):
            st.switch_page("pages/profile.py")
        if st.button("Settings", key="settings_menu", use_container_width=True):
            st.switch_page("pages/settings.py")
        if st.button("Logout", key="logout_menu", use_container_width=True):
            st.switch_page("app.py")

if "toast" in st.session_state:
    st.success(st.session_state["toast"])

# ---------------- HERO SECTION ----------------
hero_col, visual_col = st.columns([1.25, 0.8], gap="large")

with hero_col:
    st.markdown(
        """
        <div class="hero-shell">
            <div class="hero-eyebrow">✨ Smart career guidance • Powered by Gemini AI</div>
            <h1>Welcome to <span>CareerPilot AI</span></h1>
            <div class="hero-subtitle">Your personal career companion powered by AI.</div>
            <p>Turn resumes, interviews, learning plans, and career decisions into one polished growth system that helps you move forward with clarity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_cols = st.columns([5, 0.8])
    with search_cols[0]:
        question = st.text_input(
            "",
            key="home_search",
            placeholder=f"Hi {name}! How can I help you today?",
            label_visibility="collapsed",
        )
    with search_cols[1]:
        if st.button("➜", key="home_search_button", use_container_width=True):
            if question:
                with st.spinner("Thinking..."):
                    answer = ask_gemini(question)
                st.session_state["home_answer"] = answer
            else:
                st.session_state["home_answer"] = "Please share what you want help with and I will guide you."

    if st.session_state.get("home_answer"):
        st.markdown("### ✨ CareerPilot Insight")
        st.info(st.session_state["home_answer"])

    st.markdown("</div>", unsafe_allow_html=True)

with visual_col:
    st.markdown("<div class='hero-visual'>", unsafe_allow_html=True)
    render_hero_visual()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------------- FEATURE CARDS ----------------
feature_cols = st.columns(4, gap="large")

feature_cards = [
    ("📄 Resume Analyzer", "resume", "Improve ATS score and polish your resume for the next opportunity.", "Open Resume", "pages/resume.py", "feature-card resume"),
    ("💼 Career Advisor", "career", "Get expert career guidance tailored to your goals and strengths.", "Get Advice", "pages/career.py", "feature-card career"),
    ("🎤 Interview Coach", "interview", "Practice mock interviews and sharpen your communication skills.", "Practice", "pages/interview.py", "feature-card interview"),
    ("🗺 Learning Roadmap", "roadmap", "Generate a step-by-step learning path aligned with your next milestone.", "Generate", "pages/roadmap.py", "feature-card roadmap"),
]

for index, (title, page_key, description, button_label, target, card_class) in enumerate(feature_cards):
    with feature_cols[index]:
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='feature-icon'>{title.split()[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{description}</p>", unsafe_allow_html=True)
        if st.button(button_label, key=f"feature_{page_key}", use_container_width=True):
            st.switch_page(target)
        st.markdown("</div>", unsafe_allow_html=True)

st.write("")

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