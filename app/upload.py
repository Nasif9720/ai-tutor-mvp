import os
import tempfile
import streamlit as st
from crew import upload_crew


def upload_content_ui():
    """
    UI for uploading and ingesting learning content.
    """
    st.header("Upload Learning Content")
    uploaded_file = st.file_uploader(
        "Upload PDF, CSV, XLSX or ZIP", type=["pdf", "csv", "xlsx", "zip"]
    )
    if uploaded_file and st.button("Process Content"):
        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            result = upload_crew.kickoff(inputs={"file_path": tmp.name})
        st.success(result)
