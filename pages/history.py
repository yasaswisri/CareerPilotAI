import streamlit as st
import sqlite3
from components.sidebar import show_sidebar

conn = sqlite3.connect("careerpilot.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(page_title="History", layout="wide")
st.session_state["current_page"] = "history"
show_sidebar()

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #f6ebff 0%, #e9dcff 55%, #efe6ff 100%) !important; }
    section[data-testid="main"] { background: transparent; }
    div.block-container {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(109,74,255,0.16);
        border-radius: 24px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 12px 30px rgba(80,54,170,0.12);
    }
    section[data-testid="stSidebar"] { background: linear-gradient(135deg, #184a8f 0%, #4b7fe8 100%) !important; color: #ffffff !important; }
    section[data-testid="stSidebar"] .profile-name,
    section[data-testid="stSidebar"] .profile-email,
    section[data-testid="stSidebar"] .sidebar-header h2,
    section[data-testid="stSidebar"] .sidebar-header p,
    section[data-testid="stSidebar"] .sidebar-quote h4,
    section[data-testid="stSidebar"] .sidebar-quote p,
    section[data-testid="stSidebar"] .sidebar-quote small { color: #ffffff !important; }
    section[data-testid="stSidebar"] .stButton > button { background: rgba(255,255,255,0.16) !important; color: #ffffff !important; border: 1px solid rgba(255,255,255,0.24) !important; border-radius: 999px !important; }
    .page-title { font-size: 2.2rem; font-weight: 800; color: #5b21b6; margin-bottom: 0.3rem; }
    .page-subtitle { color: #4b5563; margin-bottom: 1rem; }
    .glass-card {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(109,74,255,0.16);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 26px rgba(80,54,170,0.08);
        backdrop-filter: blur(10px);
    }
    .history-pill {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        background: linear-gradient(135deg, #ede9fe, #ddd6fe);
        color: #5b21b6;
        font-size: 0.82rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }
    .empty-state {
        text-align: center;
        padding: 2rem 1rem;
        border: 1px dashed rgba(109,74,255,0.3);
        border-radius: 20px;
        background: rgba(255,255,255,0.72);
        color: #4b5563;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6d4aff, #4f46e5) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
        box-shadow: 0 8px 16px rgba(109,74,255,0.18) !important;
        transition: transform 180ms ease, box-shadow 180ms ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px rgba(109,74,255,0.24) !important;
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

st.markdown("<div class='page-title'>🕘 History</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>View all your previous AI activities.</div>", unsafe_allow_html=True)

st.markdown("""
<div class='glass-card' style='margin-bottom: 1rem;'>
    <strong>History Categories</strong><br>
    <span class='history-pill'>Resume Analyzer History</span>
    <span class='history-pill'>Career Advisor History</span>
    <span class='history-pill'>Interview Coach History</span>
    <span class='history-pill'>Learning Roadmap History</span>
</div>
""", unsafe_allow_html=True)

email = st.session_state.get("email", "")

cursor.execute("""
SELECT id,module,result,created_at
FROM history
WHERE email=?
ORDER BY created_at DESC
""", (email,))

rows = cursor.fetchall()
st.write("Logged in email:", email)
st.write("History rows:", rows)
history_items = []

for row in rows:
    history_items.append({
        "id": row[0],
        "tool": row[1],
        "summary": row[2],
        "date": row[3],
        "status": "Completed"
    })

if history_items:
    for item in history_items:
        col1, col2, col3, col4 = st.columns([2.0, 1.4, 1.6, 0.9])
        with col1:
            st.markdown(
                f"<div class='glass-card'><strong>{item['tool']}</strong><br>{item['summary']}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(f"<div class='glass-card'>{item['date']}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='glass-card'><span class='history-pill'>{item['status']}</span></div>", unsafe_allow_html=True)
        with col4:
            button_col1, button_col2 = st.columns(2)
            with button_col1:
                if st.button("👁", key=f"view_{item['id']}", use_container_width=True):
                 st.info(item["summary"])
            with button_col2:
                if st.button("🗑", key=f"delete_{item['id']}", use_container_width=True):
                  cursor.execute(
        "DELETE FROM history WHERE id=?",
        (item["id"],)
    )
    conn.commit()
    st.rerun()
else:
    st.markdown(
        """
        <div class='empty-state'>
            <h3>🕘 No history found</h3>
            <p>Your AI activities will appear here after you use CareerPilot AI.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🧹 Clear All History", use_container_width=True):
    cursor.execute(
        "DELETE FROM history WHERE email=?",
        (email,)
    )
    conn.commit()
    st.success("History Cleared")
    st.rerun()