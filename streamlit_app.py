import streamlit as st
import requests

st.title('PDF-QA — Tester')

BACKEND_URL = st.text_input('Backend URL', value='http://localhost:8000')

uploaded = st.file_uploader('Upload PDFs (multiple allowed)', type=['pdf'], accept_multiple_files=True)
if st.button('Upload') and uploaded:
    # send bytes for each uploaded file to requests
    files = [('files', (f.name, f.read(), 'application/pdf')) for f in uploaded]
    try:
        resp = requests.post(f'{BACKEND_URL}/upload', files=files, timeout=30)
        try:
            st.json(resp.json())
        except ValueError:
            st.text(resp.text)
    except requests.RequestException as e:
        st.error(f'Upload failed: {e}')

question = st.text_input('Question')
if st.button('Ask') and question:
    try:
        resp = requests.post(f'{BACKEND_URL}/query', json={'question': question, 'top_k': 4}, timeout=30)
        try:
            st.json(resp.json())
        except ValueError:
            st.text(resp.text)
    except requests.RequestException as e:
        st.error(f'Query failed: {e}')