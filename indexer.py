from typing import List, Dict
import os

import chromadb
from sentence_transformers import SentenceTransformer
from config import PERSIST_DIR, EMBEDDING_BACKEND, EMBEDDING_MODEL

# create a persistent client that reads/writes to PERSIST_DIR
# ensure PERSIST_DIR exists
os.makedirs(PERSIST_DIR, exist_ok=True)
client = chromadb.PersistentClient(path=PERSIST_DIR)

# get or create collection for PDF chunks
collection = client.get_or_create_collection(name="pdf_chunks")

# initialize embedding model only if requested
sbert = None
if EMBEDDING_BACKEND == "sentence_transformers":
    sbert = SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Return embeddings for a list of texts as a list of list of floats.
    Uses SentenceTransformer if EMBEDDING_BACKEND is set accordingly.
    """
    if EMBEDDING_BACKEND == "sentence_transformers":
        if sbert is None:
            raise RuntimeError("SentenceTransformer model not initialized.")
        emb = sbert.encode(texts, show_progress_bar=False)
        # sbert.encode returns a numpy array — convert to list of lists
        return emb.tolist()
    else:
        raise RuntimeError("Unsupported embedding backend: %s" % EMBEDDING_BACKEND)


def add_chunks_to_index(docs: List[str], metadatas: List[dict], ids: List[str]):
    """
    Add documents, metadatas and embeddings to the chroma collection and persist.
    """
    emb = embed_texts(docs)
    collection.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=emb)
    client.persist()


def query_index(query_embedding: List[float], n_results: int = 4):
    """
    Query the chroma collection using a precomputed embedding vector.
    Returns collection query result.
    """
    res = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "documents", "distances"],
    )
    return res


def get_embedding_for_text(text: str):
    return embed_texts([text])[0]
