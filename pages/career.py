import streamlit as st
from components.sidebar import navigate_to, show_sidebar
from tools.gemini_client import ask_gemini

st.set_page_config(
    page_title="Career Advisor",
    page_icon="💼",
    layout="wide"
)
st.session_state["current_page"] = "career"
show_sidebar()

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f6ebff 0%, #e9dcff 55%, #efe6ff 100%) !important;
    }
    section[data-testid="main"] {
        background: transparent;
    }
    div.block-container {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(109, 74, 255, 0.16);
        border-radius: 24px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 12px 30px rgba(80, 54, 170, 0.12);
    }
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
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.16) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.24) !important;
        border-radius: 999px !important;
    }

    .st-emotion-cache-1y4p8pa, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1wmy9hl, .st-emotion-cache-1n2fxfe {
        color: #5b21b6 !important;
    }

    div[data-testid="stVerticalBlock"] > div > label,
    div[data-testid="stVerticalBlock"] > div > div > label,
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stButton > button,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown p {
        color: #5b21b6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- TITLE ----------------

st.markdown("""
<h1 style='font-size:55px;font-weight:800;color:#6C63FF;'>
💼 AI Career Advisor
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='color:gray'>
Discover the best career path based on your skills, interests and goals.
</h4>
""", unsafe_allow_html=True)

st.write("")

# ---------------- TWO COLUMN LAYOUT ----------------

left, right = st.columns([2,1])

with left:

    st.markdown("### Tell us about yourself")

    education = st.selectbox(
        "Highest Qualification",
        [
            "High School",
            "Diploma",
            "Bachelor's Degree",
            "Master's Degree",
            "PhD"
        ]
    )

    field = st.text_input(
        "Field / Branch",
        placeholder="Example: Computer Science Engineering"
    )

    skills = st.text_area(
        "Your Skills",
        placeholder="Python, Java, SQL, HTML, CSS..."
    )

    interests = st.text_area(
        "Career Interests",
        placeholder="Artificial Intelligence, Web Development, Data Science..."
    )

    goal = st.text_input(
        "Dream Career",
        placeholder="Example: AI Engineer"
    )

    if st.button("🚀 Generate Career Plan", use_container_width=True):

        prompt = f"""
You are an expert Career Advisor.

Analyze this student's profile.

Education:
{education}

Field:
{field}

Skills:
{skills}

Interests:
{interests}

Dream Job:
{goal}

Generate:

1. Career Summary

2. Best Career Paths

3. Skill Gap Analysis

4. Skills to Learn

5. Recommended Certifications

6. Top Companies

7. Expected Salary (India)

8. 6-Month Learning Plan

9. Interview Preparation Tips

10. Final Advice
"""

        with st.spinner("Creating your AI Career Plan..."):
            result = ask_gemini(prompt)

        st.success("✅ Career Plan Generated")

        st.markdown(
            """
            <style>
            .career-result-box {
                background: #ffffff !important;
                border: 1px solid rgba(109, 74, 255, 0.16) !important;
                border-radius: 18px !important;
                padding: 1rem 1.15rem !important;
                box-shadow: 0 8px 22px rgba(80, 54, 170, 0.08) !important;
                margin-top: 0.75rem !important;
                color: #111827 !important;
                line-height: 1.7 !important;
            }
            .career-result-box p,
            .career-result-box li,
            .career-result-box strong,
            .career-result-box em,
            .career-result-box span,
            .career-result-box div {
                color: #111827 !important;
            }
            .career-result-box h1,
            .career-result-box h2,
            .career-result-box h3,
            .career-result-box h4,
            .career-result-box h5,
            .career-result-box h6 {
                color: #312e81 !important;
                margin-top: 0.6rem !important;
                margin-bottom: 0.35rem !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='career-result-box'>{result}</div>", unsafe_allow_html=True)

        st.download_button(
            "📥 Download Career Plan",
            result,
            file_name="Career_Plan.txt"
        )

with right:

    st.info("""
### 💡 Career Tips

✅ Mention all your technical skills.

✅ Mention your certifications.

✅ Mention your projects.

✅ Mention your dream company.

✅ Mention your career interests.
""")

    st.success("""
### 🚀 CareerPilot AI

Your AI mentor for:

📄 Resume Analysis

💼 Career Guidance

🎤 Interview Preparation

🗺 Learning Roadmaps
""")