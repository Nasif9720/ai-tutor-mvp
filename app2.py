# app.py
import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew
from agents import receiver_agent, tutor_agent
from tasks import upload_content, student_question

# Load environment and set page
load_dotenv()
st.set_page_config(page_title="AI Tutor", layout="centered")

# Initialize Crew once
crew = Crew(
    agents=[receiver_agent, tutor_agent],
    tasks=[upload_content, student_question],
    verbose=True
)

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Choose a page", ["📚 Upload Content", "🎓 Ask a Question"])

if page == "📚 Upload Content":
    st.title("Upload Learning Content")
    file = st.file_uploader(
        "Upload PDF/CSV/XLSX or ZIP folder", type=["pdf", "csv", "xlsx", "zip"])
    if file and st.button("Process"):
        suffix = os.path.splitext(file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            res = crew.kickoff(inputs={"file_path": tmp.name})
        st.success(res)

elif page == "🎓 Ask a Question":
    st.title("Ask Your AI Tutor")
    q = st.text_input("Enter your question")
    if q and st.button("Get Answer"):
        res = crew.kickoff(inputs={"student_question": q})
        st.markdown(res)
