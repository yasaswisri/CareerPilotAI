import streamlit as st
from components.sidebar import show_sidebar

st.set_page_config(page_title="Saved", layout="wide")
st.session_state["current_page"] = "saved"
show_sidebar()

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #f6ebff 0%, #e9dcff 55%, #efe6ff 100%) !important; }
    section[data-testid="main"] { background: transparent; }
    div.block-container { background: rgba(255,255,255,0.82); border: 1px solid rgba(109,74,255,0.16); border-radius: 24px; padding: 1.3rem 1.5rem; box-shadow: 0 12px 30px rgba(80,54,170,0.12); }
    section[data-testid="stSidebar"] { background: linear-gradient(135deg, #184a8f 0%, #4b7fe8 100%) !important; color: #ffffff !important; }
    section[data-testid="stSidebar"] .profile-name, section[data-testid="stSidebar"] .profile-email, section[data-testid="stSidebar"] .sidebar-header h2, section[data-testid="stSidebar"] .sidebar-header p, section[data-testid="stSidebar"] .sidebar-quote h4, section[data-testid="stSidebar"] .sidebar-quote p, section[data-testid="stSidebar"] .sidebar-quote small { color: #ffffff !important; }
    section[data-testid="stSidebar"] .stButton > button { background: rgba(255,255,255,0.16) !important; color: #ffffff !important; border: 1px solid rgba(255,255,255,0.24) !important; border-radius: 999px !important; }
    .page-title { font-size: 2.2rem; font-weight: 800; color: #5b21b6; margin-bottom: 0.3rem; }
    .page-subtitle { color: #4b5563; margin-bottom: 1rem; }
    .card { background: rgba(255,255,255,0.9); border: 1px solid rgba(109,74,255,0.16); border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(80,54,170,0.08); }
    .stButton > button {
        background: linear-gradient(135deg, #6d4aff, #4f46e5) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
        box-shadow: 0 8px 16px rgba(109,74,255,0.18) !important;
    }
    div[data-testid="stVerticalBlock"] label,
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stCheckbox label,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown p,
    .stMarkdown strong {
        color: #5b21b6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='page-title'>🔖 Saved</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Keep your favorite resumes, career advice, interviews, and roadmaps in one place.</div>", unsafe_allow_html=True)

if "saved_items" not in st.session_state:
    st.session_state["saved_items"] = [
        {
            "title": "Resume",
            "detail": "Senior Product Manager resume",
            "category": "Resume",
            "content": "Resume content preview for Senior Product Manager role.",
        },
        {
            "title": "Career Advice",
            "detail": "Data Science career plan",
            "category": "Career Advice",
            "content": "Career guidance summary for a Data Science transition.",
        },
        {
            "title": "Interview Questions",
            "detail": "Machine Learning interview pack",
            "category": "Interview Questions",
            "content": "Mock interview questions and answer guidance for ML roles.",
        },
    ]

for item in st.session_state["saved_items"]:
    col1, col2, col3, col4, col5 = st.columns([2.0, 1.4, 0.9, 0.9, 0.9])
    with col1:
        st.markdown(
            f"<div class='card'><strong>{item['title']}</strong><br>{item['detail']}</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(f"<div class='card'><strong>Category:</strong> {item['category']}</div>", unsafe_allow_html=True)
    with col3:
        if st.button("Open", key=f"open_{item['title']}", use_container_width=True):
            st.session_state["saved_preview"] = item
            st.success(f"Opened {item['title']}")
    with col4:
        if st.button("Remove", key=f"remove_{item['title']}", use_container_width=True):
            st.session_state["saved_items"] = [
                saved_item for saved_item in st.session_state["saved_items"] if saved_item["title"] != item["title"]
            ]
            st.experimental_rerun()
    with col5:
        if st.button("Download", key=f"download_{item['title']}", use_container_width=True):
            st.download_button(
                label="Download",
                data=item["content"],
                file_name=f"{item['title']}.txt",
                mime="text/plain",
                key=f"download_data_{item['title']}",
            )

if st.session_state.get("saved_preview"):
    preview = st.session_state["saved_preview"]
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='card'><h3>Preview: {preview['title']}</h3><p>{preview['content']}</p></div>",
        unsafe_allow_html=True,
    )

if not st.session_state["saved_items"]:
    st.markdown(
        """
        <div class='card' style='margin-top: 1rem; text-align: center; color: #4b5563;'>
            <h3>📭 No saved items</h3>
            <p>Your favorite career resources will appear here when you save them.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
