# crew.py

from crewai import Crew
from agents import receiver_agent, tutor_agent, question_agent, feedback_agent, mentor_agent
from tasks import upload_content, student_question, generate_question_task, evaluate_answer_task, mentor_task

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

mentor_crew = Crew(
    agents=[mentor_agent],
    tasks=[mentor_task],
    verbose=True
)
