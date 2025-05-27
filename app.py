import streamlit as st
from db.db import init_db
from app.router import run_app


def main():
    st.set_page_config(page_title="AI Tutor", layout="centered")
    init_db()
    run_app()


if __name__ == "__main__":
    main()
