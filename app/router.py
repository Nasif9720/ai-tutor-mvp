import streamlit as st
from app.upload import upload_content_ui
from app.tutor import tutor_ui
from app.assessment import assessment_ui


def run_app():
    st.title("AI Tutor")
    action = st.radio(
        "Select an action:",
        ("Upload Content", "Ask a Question", "Challenge Assessment")
    )

    if action == "Upload Content":
        upload_content_ui()
    elif action == "Ask a Question":
        tutor_ui()
    elif action == "Challenge Assessment":
        assessment_ui()
