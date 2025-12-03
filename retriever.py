from typing import List, Dict
from indexer import get_embedding_for_text, query_index
from config import SIMILARITY_DISTANCE_THRESHOLD
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def search_pdfs(question: str, top_k: int = 4):
    emb = get_embedding_for_text(question)
    res = query_index(emb, n_results=top_k)
    docs = []
    if res and res.get('ids'):
        doks = res['documents'][0]
        metas = res['metadatas'][0]
        dists = res['distances'][0]
        for doc, meta, dist in zip(doks, metas, dists):
            docs.append({"text": doc, "meta": meta, "distance": dist})
    return docs

def best_is_relevant(docs):
    if not docs:
        return False
    best = docs[0]
    return best['distance'] <= SIMILARITY_DISTANCE_THRESHOLD

def synthesize_answer_from_docs(question: str, docs: List[Dict]):
    context = "\n\n".join([
        f"File: {d['meta']['pdf_name']} | Page: {d['meta']['page_no']}\n{d['text']}" for d in docs
    ])
    prompt = (
        "You are an assistant that answers questions using only the provided passages.\n"
        "If the passages don't contain the answer, say you don't know. Cite sources using file and page number.\n\n"
        f"Passages:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=500,
        temperature=0.0
    )
    return resp['choices'][0]['message']['content']

def fallback_openai_answer(question: str):
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": f"Answer the question: {question}"}],
        max_tokens=500,
        temperature=0.0
    )
    return resp['choices'][0]['message']['content']

def answer_question(question: str, top_k: int = 4):
    docs = search_pdfs(question, top_k=top_k)
    if not docs or not best_is_relevant(docs):
        return {"source": "openai_fallback", "answer": fallback_openai_answer(question)}
    answer = synthesize_answer_from_docs(question, docs)
    sources = [
        {"pdf_name": d['meta']['pdf_name'], "page_no": d['meta']['page_no'], "snippet": d['text'][:300], "distance": d['distance']}
        for d in docs
    ]
    return {"source": "pdf", "answer": answer, "sources": sources}
