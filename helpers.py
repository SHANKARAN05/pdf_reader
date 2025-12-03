from typing import List
import re
from config import CHUNK_WORD_SIZE, CHUNK_OVERLAP

_whitespace_re = re.compile(r"\s+")

def clean_text(text: str) -> str:
    if not text:
        return ""
    t = text.replace("\x0c", " ")
    t = _whitespace_re.sub(" ", t).strip()
    return t

def chunk_text_words(text: str, chunk_size: int = CHUNK_WORD_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    start = 0
    n = len(words)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == n:
            break
        start = end - overlap
    return chunks
