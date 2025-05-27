# crew.py
from dotenv import load_dotenv
from crewai import Crew
from agents import receiver_agent, tutor_agent
from tasks import upload_content, student_question


def main():
    # Load .env so API key is available
    load_dotenv()

    crew = Crew(
        agents=[receiver_agent, tutor_agent],
        tasks=[upload_content, student_question],
        verbose=True
    )

    mode = input("Choose mode [upload/ask]: ").strip().lower()
    if mode == "upload":
        path = input("Enter path to file (PDF/CSV/XLSX/ZIP/dir): ").strip()
        result = crew.kickoff(inputs={"file_path": path})
        print(result)

    elif mode == "ask":
        q = input("Enter your question: ").strip()
        result = crew.kickoff(inputs={"student_question": q})
        print(result)

    else:
        print("Invalid option. Please choose 'upload' or 'ask'.")


if __name__ == "__main__":
    main()
