# app/assessment.py
import streamlit as st
from crew import question_crew, feedback_crew
from db.db import save_feedback  # ← import the saver


def assessment_ui():
    if "question" not in st.session_state:
        st.info("Please ask a question first in the 'Ask a Question' tab.")
        return

    st.divider()
    st.subheader("🧠 Challenge Assessment")

    # 1) Generate challenge question
    if st.button("Generate Challenge Question"):
        topic = st.session_state["question"]
        q_out = question_crew.kickoff(inputs={"question": topic})
        challenge = q_out.tasks_output[0].raw
        st.session_state["challenge"] = challenge

    # 2) Show and answer the challenge
    if "challenge" in st.session_state:
        st.markdown(f"**Challenge Question:** {st.session_state['challenge']}")
        student_answer = st.text_area("Your Answer to the Challenge:")

        # 3) Submit and save feedback
        if st.button("Submit Answer") and student_answer:
            fb_out = feedback_crew.kickoff(inputs={
                "question": st.session_state["challenge"],
                "student_answer": student_answer
            })
            feedback_text = fb_out.tasks_output[0].raw

            # Display it
            st.markdown("### 📋 Feedback")
            st.markdown(feedback_text)

            # Persist it
            save_feedback(
                student_id="guest_001",                        # replace with real user ID later
                question=st.session_state["question"],
                challenge_question=st.session_state["challenge"],
                student_answer=student_answer,
                feedback=feedback_text,
                score=None  # or parse out a numeric score from feedback_text
            )
            st.success("Your answer & feedback have been saved.")
