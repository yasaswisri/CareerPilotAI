import streamlit as st

from auth import get_user_profile, load_session


def sync_user_context():
    session_data = load_session()
    if session_data:
        st.session_state["authenticated"] = session_data.get("authenticated", False)
        st.session_state["remember_me"] = session_data.get("remember_me", False)
        st.session_state["name"] = session_data.get("name") or st.session_state.get("name", "Guest")
        st.session_state["email"] = session_data.get("email") or st.session_state.get("email", "guest@example.com")
        st.session_state["profile_picture"] = session_data.get("profile_picture") or st.session_state.get("profile_picture")

    if not st.session_state.get("authenticated"):
        st.session_state.setdefault("name", "Guest")
        st.session_state.setdefault("email", "guest@example.com")

    st.session_state.setdefault("theme_mode", "light")
    st.session_state.setdefault("profile_picture", None)

    if st.session_state.get("authenticated") and st.session_state.get("email"):
        profile_data = get_user_profile(st.session_state.get("email", "")) or {}
        if profile_data.get("theme_mode"):
            st.session_state["theme_mode"] = profile_data.get("theme_mode", "light")

    if st.session_state.get("theme_mode") not in {"light", "dark", "system"}:
        st.session_state["theme_mode"] = "light"


def get_display_user_info():
    name = st.session_state.get("name") or "Guest"
    if not name or name == "None":
        name = "Guest"

    email = st.session_state.get("email") or "guest@example.com"
    if not email or email == "None":
        email = "guest@example.com"

    return name, email, st.session_state.get("profile_picture")


def apply_theme_css():
    theme_mode = st.session_state.get("theme_mode", "light")

    if theme_mode == "dark":
        css = """
        :root {
            --app-bg: #060816;
            --surface: #111827;
            --surface-2: #1f2937;
            --text: #f9fafb;
            --muted: #cbd5e1;
            --border: rgba(255,255,255,0.12);
            --accent: #8b5cf6;
            --accent-2: #3b82f6;
        }
        """
    elif theme_mode == "system":
        css = """
        @media (prefers-color-scheme: dark) {
            :root {
                --app-bg: #060816;
                --surface: #111827;
                --surface-2: #1f2937;
                --text: #f9fafb;
                --muted: #cbd5e1;
                --border: rgba(255,255,255,0.12);
                --accent: #8b5cf6;
                --accent-2: #3b82f6;
            }
        }
        """
    else:
        css = """
        :root {
            --app-bg: #f7f8ff;
            --surface: #ffffff;
            --surface-2: #f3f4f6;
            --text: #111827;
            --muted: #6b7280;
            --border: rgba(15,23,42,0.08);
            --accent: #6d4aff;
            --accent-2: #4f46e5;
        }
        """

    st.markdown(
        f"""
        <style>
        {css}
        [data-testid="stAppViewContainer"] {{ background: var(--app-bg) !important; }}
        section[data-testid="main"] {{ background: transparent; }}
        .block-container {{ background: var(--surface) !important; border: 1px solid var(--border); border-radius: 24px; padding: 1.3rem 1.5rem; box-shadow: 0 12px 30px rgba(80,54,170,0.12); }}
        .page-title, .page-subtitle, .card h3, .stMarkdown h3, .stMarkdown h4, .stMarkdown p, .stMarkdown strong {{ color: var(--text) !important; }}
        .page-subtitle, .stMarkdown p {{ color: var(--muted) !important; }}
        .card {{ background: var(--surface-2); border: 1px solid var(--border); border-radius: 18px; padding: 1rem; margin-bottom: 1rem; }}
        .stButton > button {{ background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important; color: white !important; border: none !important; border-radius: 999px !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
