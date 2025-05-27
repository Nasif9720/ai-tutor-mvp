import re
import streamlit as st
from crew import tutor_crew


def tutor_ui():
    """
    UI for student to ask a question and display tutor's answer.
    """
    st.header("Ask Your AI Tutor")
    question = st.text_input("Enter your question here:")
    if question and st.button("Get Answer"):
        tutor_result = tutor_crew.kickoff(
            inputs={"student_question": question})
        answer = tutor_result.tasks_output[0].raw
        # Render answer with LaTeX blocks
        parts = re.split(r'(\$\$.*?\$\$)', answer, flags=re.DOTALL)
        for part in parts:
            if part.startswith("$$") and part.endswith("$$"):
                st.latex(part.strip("$$"))
            else:
                st.markdown(part)
        # Save the topic for assessment
        st.session_state["question"] = question
