import streamlit as st
from components.sidebar import show_sidebar
from tools.gemini_client import ask_gemini

st.set_page_config(
    page_title="Career Advisor",
    page_icon="💼",
    layout="wide"
)

show_sidebar()

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

        st.markdown(result)

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