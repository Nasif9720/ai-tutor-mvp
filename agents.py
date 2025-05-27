# agents.py
from dotenv import load_dotenv
from crewai import Agent
from tools import llm, rag_tool

# Ensure .env is loaded (so rag_tool and llm have creds)
load_dotenv()

receiver_agent = Agent(
    role="Receiver Agent",
    goal="Ingest uploaded files into the knowledge base",
    backstory="You chunk, embed, and index any PDF, TXT, CSV, XLSX, or folder so it’s searchable.",
    tools=[rag_tool],
    llm=llm,
    verbose=True
)

tutor_agent = Agent(
    role="Tutor Agent",
    goal="Answer student's question using the indexed content",
    backstory="You retrieve relevant chunks and respond with clear, structured explanations and examples.",
    tools=[rag_tool],
    llm=llm,
    verbose=True
)

# Agent to generate a challenge question
question_agent = Agent(
    role="Challenge Question Generator",
    goal="Design thoughtful open-ended assessment questions on the topic",
    backstory="You're a seasoned educator who knows how to challenge students with questions that make them think deeply.",
    tools=[rag_tool],
    llm=llm,
    verbose=True
)

# Agent to evaluate student answers
feedback_agent = Agent(
    role="Answer Evaluator",
    goal="Provide constructive and encouraging feedback to student answers with a score out of 10",
    backstory="You're a kind and expert teacher who evaluates student answers on {question} by highlighting what they did well and where they can improve.",
    tools=[rag_tool],
    llm=llm,
    verbose=True
)
