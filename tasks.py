# tasks.py
from crewai import Task
from agents import receiver_agent, tutor_agent, question_agent, feedback_agent, mentor_agent
from tools import ingest_file, generate_answer, generate_quiz_from_context, retrieve_docs, get_flat_context, generate_mentor_guidance

upload_content = Task(
    description=(
        "Index the uploaded file into the vector knowledge base by "
        "wiping any existing index and embedding this file."
    ),
    expected_output=(
        "A confirmation message that the old index was cleared "
        "and the new file was indexed successfully."
    ),
    agent=receiver_agent,
    async_execution=False,
    output_function=lambda inputs: ingest_file(inputs["file_path"])
)

student_question = Task(
    description=(
        "Answer the student's by retrieving the most relevant on {student_question} "
        "content from the indexed knowledge base and formatting the response."
    ),
    expected_output=(
        "A structured answer with sections (Summary, Explanation, Mathmatical Formula if applicable, Examples, Tips)."
        "keep the mathmatical formula in format of MathJax with a line break."
    ),
    agent=tutor_agent,
    async_execution=False,
    output_function=lambda inputs: generate_answer(inputs["student_question"])
)

generate_question_task = Task(
    description="Generate a thoughtful open-ended assessment question based on the topic {question}.",
    expected_output="A clear, challenging, and concise question for the student."
    "You are asking the question directly to the student.",
    agent=question_agent,
    async_execution=False
)

evaluate_answer_task = Task(
    description="Evaluate the student's answer to the question: {question}. The student's answer is: {student_answer}. Provide constructive feedback and a score out of 10.",
    expected_output="Constructive feedback"
    "Provide what could have better and what was done well in the answer. "
    "The feedback should be encouraging and helpful for the student to improve."
    "Provide a score out of 10 for the {student_answer}.",
    agent=feedback_agent,
    async_execution=False,
)


mentor_task = Task(
    description="Provide personalized study guidance for student `{student_id}` based on their past assessment history.",
    expected_output="A structured roadmap with review topics, next steps, and study tips.",
    agent=mentor_agent,
    async_execution=False,
    output_function=lambda inputs: generate_mentor_guidance(
        inputs["student_id"])
)
