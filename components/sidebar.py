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

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="brand-badge">CP</div>
                <div>
                    <h2>CareerPilot AI</h2>
                    <p>Your AI Career Coach</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        name = st.session_state.get("name", "Guest")
        email = st.session_state.get("email", "")

        st.markdown(
            f"""
            <div class="sidebar-profile">
                <div class="profile-avatar">{name[:1].upper()}</div>
                <div class="profile-copy">
                    <div class="profile-name">{name}</div>
                    <div class="profile-email">{email or 'Welcome back'}</div>
                </div>
                <span class="online-dot"></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='sidebar-nav-group'>", unsafe_allow_html=True)
        nav_items = [
            ("🏠 Home", "home", "pages/home.py"),
            ("💼 Career Advisor", "career", "pages/career.py"),
            ("📄 Resume Analyzer", "resume", "pages/resume.py"),
            ("🎤 Interview Coach", "interview", "pages/interview.py"),
            ("🗺 Learning Roadmap", "roadmap", "pages/roadmap.py"),
        ]

        for label, page_key, target in nav_items:
            if current_page == page_key:
                st.markdown(
                    f"<div class='nav-item active'><span class='nav-icon'>{label.split()[0]}</span><span>{label.split(' ', 1)[1]}</span></div>",
                    unsafe_allow_html=True,
                )
            else:
                if st.button(label, key=f"sidebar_{page_key}", use_container_width=True):
                    navigate_to(page_key, target)

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        secondary_items = [
            ("🕘 History", "history", "components/history.py"),
            ("❤️ Saved", "saved", "components/saved.py"),
            ("👤 Profile", "profile", "pages/profile.py"),
            ("⚙ Settings", "settings", "pages/settings.py"),
        ]

        for label, page_key, target in secondary_items:
            if current_page == page_key:
                st.markdown(
                    f"<div class='nav-item active'><span class='nav-icon'>{label.split()[0]}</span><span>{label.split(' ', 1)[1]}</span></div>",
                    unsafe_allow_html=True,
                )
            else:
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

        st.markdown("<div class='sidebar-footer'>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)