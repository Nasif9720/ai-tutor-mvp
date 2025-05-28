# db/db.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.sqlite3")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                question TEXT,
                challenge_question TEXT,
                student_answer TEXT,
                feedback TEXT,
                score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_feedback(student_id, question, challenge_question,
                  student_answer, feedback, score=None):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO feedback (
                student_id, question, challenge_question,
                student_answer, feedback, score
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, question, challenge_question,
              student_answer, feedback, score))
        conn.commit()


def get_feedback_by_student(student_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT question,
                   challenge_question,
                   student_answer,
                   feedback,
                   score,
                   timestamp
              FROM feedback
             WHERE student_id = ?
             ORDER BY timestamp DESC
        """, (student_id,))
        return c.fetchall()
