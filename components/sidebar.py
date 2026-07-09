import os
import sys
import streamlit as st


def get_current_page_key():
    """Resolve the current page so the sidebar can highlight the active item."""
    main_module = sys.modules.get("__main__")
    main_file = getattr(main_module, "__file__", "")

    if not main_file:
        return st.session_state.get("current_page", "home")

    page_map = {
        "home.py": "home",
        "career.py": "career",
        "resume.py": "resume",
        "interview.py": "interview",
        "roadmap.py": "roadmap",
        "profile.py": "profile",
        "settings.py": "settings",
    }

    return page_map.get(os.path.basename(main_file), st.session_state.get("current_page", "home"))


def navigate_to(page_key, target_page):
    """Persist the current page and switch routes while keeping the UI intact."""
    st.session_state["current_page"] = page_key
    st.switch_page(target_page)


def show_sidebar():
    """Render the custom glassmorphism sidebar used across the app."""
    current_page = get_current_page_key()

    if current_page in {"resume", "career", "interview", "roadmap", "profile", "settings", "history", "saved"}:
        st.markdown(
            """
            <style>
            section[data-testid="stSidebar"] {
                background: linear-gradient(135deg, #184a8f 0%, #4b7fe8 100%) !important;
                color: #ffffff !important;
            }
            section[data-testid="stSidebar"] .profile-name,
            section[data-testid="stSidebar"] .profile-email,
            section[data-testid="stSidebar"] .sidebar-header h2,
            section[data-testid="stSidebar"] .sidebar-header p,
            section[data-testid="stSidebar"] .sidebar-quote h4,
            section[data-testid="stSidebar"] .sidebar-quote p,
            section[data-testid="stSidebar"] .sidebar-quote small {
                color: #ffffff !important;
            }
            section[data-testid="stSidebar"] .nav-item.active {
                background: rgba(255, 255, 255, 0.18) !important;
                color: #ffffff !important;
            }
            section[data-testid="stSidebar"] .stButton > button {
                background: rgba(255, 255, 255, 0.16) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.24) !important;
                border-radius: 999px !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    with st.sidebar:
        name = st.session_state.get("name", "Guest")

        st.markdown(
            f"""
            <div class="profile-header"><div class="profile-avatar">👤</div>
                <div class="profile-name">{name}</div>
            </div>
            <span class="online-dot"></span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sidebar-header">
                <div><h2>CareerPilot AI</h2><p>Your AI Career Coach</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='sidebar-nav-group'>", unsafe_allow_html=True)
        nav_items = [
            ("🏠 Home", "home", "pages/home.py"),
            ("📑 Resume Builder", "resume", "pages/resume.py"),
            ("💼 Career Advisor", "career", "pages/career.py"),
            ("🎤 Interview Coach", "interview", "pages/interview.py"),
            ("🗺 Learning Roadmap", "roadmap", "pages/roadmap.py"),
        ]

        st.markdown(
            """
            <style>
            [data-testid="stSidebarNav"] { display: none !important; }

            section[data-testid="stSidebar"] .stButton > button {
                transition: transform 180ms ease, box-shadow 180ms ease, background 180ms ease, border-color 180ms ease;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                overflow: hidden;
                position: relative;
            }

            section[data-testid="stSidebar"] .stButton > button:hover {
                transform: translateX(4px) scale(1.01);
                box-shadow: 0 10px 18px rgba(0, 0, 0, 0.14);
                background: rgba(255, 255, 255, 0.24) !important;
                border-color: rgba(255, 255, 255, 0.34) !important;
            }

            section[data-testid="stSidebar"] .stButton > button:focus,
            section[data-testid="stSidebar"] .stButton > button:active {
                transform: translateX(2px) scale(0.99);
                box-shadow: 0 6px 14px rgba(0, 0, 0, 0.14);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        for label, page_key, target in nav_items:
            if current_page == page_key:
                continue

            if st.button(label, key=f"sidebar_{page_key}", use_container_width=True):
                navigate_to(page_key, target)

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        secondary_items = [
            ("👤 Profile", "profile", "pages/profile.py"),
            ("⚙ Settings", "settings", "pages/settings.py"),
        ]

        for label, page_key, target in secondary_items:
            if current_page == page_key:
                continue

            if st.button(label, key=f"sidebar_{page_key}", use_container_width=True):
                navigate_to(page_key, target)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sidebar-quote'>", unsafe_allow_html=True)
        st.markdown(
            """
            <h4>✨ Daily Momentum</h4>
            <p>The best way to predict your future is to create it.</p>
            <small>— Peter Drucker</small>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        