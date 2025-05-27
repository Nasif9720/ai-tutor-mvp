# tools.py
import re
import json
import os
import shutil
from dotenv import load_dotenv
from crewai_tools import RagTool
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL_NAME"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Initial RAG tool instance (will be re-created on ingest)
rag_tool = RagTool(
    persist_directory="rag_db",
    chunk_size=800,
    chunk_overlap=150
)


def ingest_file(path: str) -> str:
    """
    Wipe the old index and ingest this file/folder into a fresh RAG store.
    Supports PDF, TXT, CSV, XLSX, and ZIP (treated as directory).
    """
    global rag_tool

    # 1) Remove existing embeddings folder
    if os.path.isdir(rag_tool.persist_directory):
        shutil.rmtree(rag_tool.persist_directory)

    # 2) Re-initialize a clean RagTool
    rag_tool = RagTool(
        persist_directory="rag_db",
        chunk_size=800,
        chunk_overlap=150
    )

    # 3) Determine data type and ingest
    ext = os.path.splitext(path)[1].lower().lstrip('.')
    dtype = {
        "pdf":  "file",
        "txt":  "file",
        "csv":  "csv",
        "xlsx": "csv",
        "zip":  "dir",
    }.get(ext, "file")

    rag_tool.add(data_type=dtype, path=path)
    return f"✅ Wiped old index and indexed '{os.path.basename(path)}' as '{dtype}'"

# Function to retrieve documents based on a query


def retrieve_docs(query: str, top_k: int = 5):
    """
    Return the top_k most relevant chunks for a query.
    """
    return rag_tool.search(query)[:top_k]

# Function to generate an answer using the LLM


def generate_answer(query: str, docs=None) -> str:
    """
    Build a prompt from the retrieved docs and call the LLM.
    """
    if docs is None:
        docs = retrieve_docs(query)

    context = "\n\n".join(doc.content for doc in docs)
    prompt = f"""
Use the following context to answer the question clearly:

{context}

Question: {query}

Respond in sections:
1. Brief Summary
2. Step-by-step Explanation
3. Examples
4. Extra Tip or Related Info
"""
    chat = llm.chat([
        {"role": "system", "content": "You are a helpful tutor."},
        {"role": "user",   "content": prompt}
    ])
    return chat.choices[0].message.content

# Function to generate a quiz based on the context and topic


def get_flat_context(query: str) -> str:
    """
    Use RagTool's `.run()` method to get a plain context string for simple use cases
    like quiz generation or display.
    """
    return rag_tool.run({"query": query})

# Function to generate a quiz based on the context and topic


def generate_quiz_from_context(topic: str):
    if not isinstance(topic, str):
        topic = str(topic)

    prompt = f"""
Generate 3-5 multiple-choice questions on the topic: "{topic}".

Format:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "..."
  }},
  ...
]
Only return a valid JSON list. Do not include explanations or anything else.
"""

    chat = llm.chat([
        {"role": "system", "content": "You are a helpful assessment quiz generator."},
        {"role": "user", "content": prompt}
    ])

    import json
    try:
        # Strictly validate that the output is a list of dicts with expected fields
        raw = chat.choices[0].message.content
        parsed = json.loads(raw)
        if isinstance(parsed, list) and all(
            isinstance(q, dict) and {"question", "options", "answer"} <= set(q)
            for q in parsed
        ):
            return parsed
        return []
    except Exception:
        return []
