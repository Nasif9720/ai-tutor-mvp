import sqlite3
import os

# Path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), 'feedback.sqlite3')


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                question TEXT,
                student_answer TEXT,
                feedback TEXT,
                score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


def save_feedback(student_id, question, student_answer, feedback, score):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (student_id, question, student_answer, feedback, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, question, student_answer, feedback, score))
        conn.commit()
