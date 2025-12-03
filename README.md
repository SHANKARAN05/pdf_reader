# pdf_reader
A complete AI-powered system that allows users to upload one or multiple PDF documents and ask questions based on the content inside them. If the answer is not found inside the PDFs, the system automatically uses OpenAI API as fallback and returns the response.
📄 PDF Question Answering System (FastAPI + Streamlit + OpenAI)

A complete AI-powered system that allows users to upload one or multiple PDF documents and ask questions based on the content inside them.
If the answer is not found inside the PDFs, the system automatically uses OpenAI API as fallback and returns the response.

🚀 Features
✅ 1. Multi-PDF Upload

Users can upload multiple PDF files simultaneously.
Each PDF is processed page-by-page, text is extracted, chunked, and indexed.

✅ 2. Answer Questions Based on PDF Content

The system searches the vector database and returns:

The exact answer

Page number

PDF name

Context snippet

✅ 3. Fallback to OpenAI

If the answer cannot be found inside the PDFs, the backend automatically sends the user query to OpenAI and returns a high-quality AI-generated answer.

✅ 4. FastAPI Backend

The backend handles:

Text extraction

OCR (for scanned PDFs)

Chunking

Vector storage

Retrieval

OpenAI fallback

All exposed via clean REST endpoints (/upload, /query).

✅ 5. Streamlit Frontend

A simple, clean UI:

PDF upload interface

Ask question textbox

Display retrieved answers

Show page number and PDF source

Option to retry using OpenAI

✅ 6. Modular Code Architecture

The project is fully modular:

processor/      → PDF extraction + OCR  
indexer/        → Vector DB indexing  
retriever/      → Semantic search  
utils/          → Helpers  
ui/             → Streamlit frontend  
main.py         → FastAPI app  

🧩 Project Workflow
1️⃣ Upload PDFs

Users upload one or multiple PDFs → backend extracts text → chunks it → stores chunks in vector DB.

2️⃣ Ask Questions

Users type a question → backend performs semantic search → returns the most relevant answer.

3️⃣ If Not Found → Call OpenAI

If no chunk crosses relevance threshold → system uses OpenAI API as fallback and returns the generated answer.

📦 Tech Stack
Backend

Python

FastAPI

Uvicorn

PyPDF / OCR

ChromaDB or FAISS

OpenAI API

Frontend

Streamlit

Others

UUID for chunk IDs

Dotenv for API keys

📂 Folder Structure
pdf_project/
│── main.py
│── requirements.txt
│── .env
│
├── processor/
│   └── pdf_extractor.py
│
├── indexer/
│   └── vector_index.py
│
├── retriever/
│   └── query_engine.py
│
├── utils/
│   └── helpers.py
│
└── ui/
    └── streamlit_app.py

▶️ Running the Project
Backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000


Open API Docs:

http://127.0.0.1:8000/docs

Frontend
streamlit run ui/streamlit_app.py


Connect UI → Backend URL:

http://127.0.0.1:8000

🎯 Use Cases

Academic research

Legal document analysis

Financial reports Q&A

Ebook assistants

Multi-PDF knowledge bases

Automated document intelligence

⭐ Future Improvements

Support for DOCX and images

Fine-tuned LLMs

Citations and answer confidence score

Cosine similarity heatmap visualization

Local LLM support (Llama / Mistral)

If you want, I can also generate:

✅ README.md full file
✅ Project banner image
✅ Badges (Python version, license, contributors, stars, etc.)
✅ License (MIT)
✅ Setup scripts
✅ API documentation
