import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import tempfile
import os

# ========= Gemini API Configuration =========
API_KEY = "AIzaSyBZloFKbyaMn0EcrK8FdWZybl0OMGITfm0"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-pro")  # Use 'pro' for higher quality

# ========= Streamlit UI Setup =========
st.set_page_config(page_title="AI Resume Generator", layout="centered", page_icon="📄")

st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to right, #ece9e6, #ffffff);
        padding: 2rem;
    }
    h1 {
        color: #0b3d91;
        text-align: center;
    }
    .stButton>button {
        background-color: #0b3d91;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 16px;
    }
    .stDownloadButton>button {
        background-color: #009688;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Generator")

with st.expander("ℹ️ Instructions"):
    st.markdown("""
    - Fill in your details below.
    - Select the job role you want to customize for.
    - Click **Generate Resume**.
    - Download it as a PDF or regenerate if needed.
    """)

# ========= User Inputs =========
name = st.text_input("👤 Full Name")
email = st.text_input("📧 Email")
phone = st.text_input("📱 Phone Number")
linkedin = st.text_input("🔗 LinkedIn URL")
skills = st.text_area("🛠️ Skills (comma separated)", placeholder="Python, AI, ML, Data Analysis")
experience = st.text_area("💼 Work Experience", placeholder="Mention your past roles, achievements...")
education = st.text_area("🎓 Education", placeholder="Degree, College, Year of passing...")

job_role = st.selectbox("🎯 Target Job Role", ["Software Developer", "Data Scientist", "AI Researcher", "Product Manager", "Cybersecurity Analyst"])

# ========= Generate Resume Prompt =========
def generate_resume(name, email, phone, linkedin, skills, experience, education, job_role):
    prompt = f"""
    Create a professional resume for the following candidate:

    Name: {name}
    Email: {email}
    Phone: {phone}
    LinkedIn: {linkedin}

    Skills: {skills}
    Experience: {experience}
    Education: {education}
    Job Role: {job_role}

    Format it in bullet points, make it concise, ATS-friendly, and include a professional summary at the top.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# ========= Resume Generation =========
if st.button("🚀 Generate Resume"):
    if name and skills and experience and education:
        with st.spinner("Generating resume..."):
            resume_text = generate_resume(name, email, phone, linkedin, skills, experience, education, job_role)
            st.session_state.resume = resume_text
    else:
        st.warning("Please fill out all required fields.")

# ========= Show Resume =========
if "resume" in st.session_state:
    st.subheader("📄 Generated Resume")
    st.text_area("Your Resume", value=st.session_state.resume, height=500)

    def create_pdf(content):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        pdf.set_auto_page_break(auto=True, margin=15)
        for line in content.split('\n'):
            pdf.multi_cell(0, 10, line)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            return tmp.name

    pdf_path = create_pdf(st.session_state.resume)
    with open(pdf_path, "rb") as file:
        st.download_button("📥 Download Resume as PDF", file, file_name="AI_Generated_Resume.pdf", mime="application/pdf")
    os.remove(pdf_path)