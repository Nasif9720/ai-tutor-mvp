import os
import re
import tempfile
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew
from agents import receiver_agent, tutor_agent, question_agent, feedback_agent
from tasks import upload_content, student_question, generate_question_task, evaluate_answer_task


def main():
    load_dotenv()
    st.set_page_config(page_title="AI Tutor", layout="centered")
    st.title("AI Tutor")

    upload_crew = Crew(
        agents=[receiver_agent],
        tasks=[upload_content],
        verbose=True
    )

    tutor_crew = Crew(
        agents=[tutor_agent],
        tasks=[student_question],
        verbose=True
    )

    question_crew = Crew(
        agents=[question_agent],
        tasks=[generate_question_task],
        verbose=True
    )

    feedback_crew = Crew(
        agents=[feedback_agent],
        tasks=[evaluate_answer_task],
        verbose=True
    )

    action = st.radio("Select an action:",
                      ("Upload Content", "Ask a Question"))

    if action == "Upload Content":
        st.header("Upload Learning Content")
        uploaded_file = st.file_uploader("Upload PDF, CSV, XLSX or ZIP", type=[
                                         "pdf", "csv", "xlsx", "zip"])
        if uploaded_file and st.button("Process Content"):
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                result = upload_crew.kickoff(inputs={"file_path": tmp.name})
            st.success(result)

    elif action == "Ask a Question":
        st.header("Ask Your AI Tutor")
        user_question = st.text_input("Enter your question here:")

        if user_question and st.button("Get Answer"):
            tutor_result = tutor_crew.kickoff(
                inputs={"student_question": user_question})
            answer = tutor_result.tasks_output[0].raw
            st.session_state["user_question"] = user_question

            parts = re.split(r'(\$\$.*?\$\$)', answer, flags=re.DOTALL)
            for part in parts:
                if part.startswith("$$") and part.endswith("$$"):
                    st.latex(part.strip("$$"))
                else:
                    st.markdown(part)

        if "user_question" in st.session_state:
            st.divider()
            st.subheader("\U0001F9E0 Take Assessment")

            if st.button("Generate Challenge Question"):
                question_result = question_crew.kickoff(
                    inputs={"question": st.session_state["user_question"]})
                st.session_state["challenge_question"] = question_result.tasks_output[0].raw

            if "challenge_question" in st.session_state:
                st.markdown(
                    f"**Challenge Question:** {st.session_state['challenge_question']}")

                student_answer = st.text_area(
                    "Your Answer:", key="student_answer")

                if st.button("Submit Answer") and student_answer:
                    feedback_result = feedback_crew.kickoff(inputs={
                        "question": st.session_state["challenge_question"],
                        "student_answer": student_answer
                    })
                    st.markdown("### \U0001F4CB Feedback")
                    st.markdown(feedback_result.tasks_output[0].raw)


if __name__ == "__main__":
    main()
