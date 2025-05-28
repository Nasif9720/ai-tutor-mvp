# app/mentor.py
import streamlit as st
from crew import mentor_crew


def mentor_ui():
    st.header("👨‍🏫 Mentor Guidance")
    student_id = st.text_input("Enter your Student ID:", value="guest_001")
    if student_id and st.button("Get Guidance"):
        out = mentor_crew.kickoff(inputs={"student_id": student_id})
        guidance = out.tasks_output[0].raw
        st.markdown(guidance)
