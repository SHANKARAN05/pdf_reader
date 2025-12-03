import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from processor import extract_pages_from_pdf_bytes
from utils.helpers import chunk_text_words
from indexer import add_chunks_to_index
from retriever import answer_question

app = FastAPI(title="PDF-QA")

@app.post('/upload')
async def upload(files: List[UploadFile] = File(...)):
    results = {}
    for f in files:
        content = await f.read()
        pages = extract_pages_from_pdf_bytes(content, use_ocr_if_empty=True)
        docs = []
        metadatas = []
        ids = []
        for p in pages:
            text = p['text']
            if not text:
                continue
            chunks = chunk_text_words(text)
            for i, chunk in enumerate(chunks):
                uid = str(uuid.uuid4())
                docs.append(chunk)
                metadatas.append({
                    'pdf_name': f.filename,
                    'page_no': p['page_no'],
                    'chunk_index': i
                })
                ids.append(uid)
        if docs:
            add_chunks_to_index(docs, metadatas, ids)
            results[f.filename] = {'added_chunks': len(docs)}
        else:
            results[f.filename] = {'added_chunks': 0}
    return {'status': 'ok', 'results': results}

@app.post('/query')
async def query(question: str, top_k: int = 4):
    if not question:
        raise HTTPException(status_code=400, detail="question required")
    res = answer_question(question, top_k=top_k)
    return res

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='0.0.0.0', port=int(os.environ.get('SERVER_PORT', 8000)), reload=True)
