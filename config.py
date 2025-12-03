import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "sentence_transformers")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
SIMILARITY_DISTANCE_THRESHOLD = float(os.getenv("SIMILARITY_DISTANCE_THRESHOLD", "0.5"))
CHUNK_WORD_SIZE = int(os.getenv("CHUNK_WORD_SIZE", "150"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "30"))
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
