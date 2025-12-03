import io
import pdfplumber
from typing import List, Dict
from utils.helpers import clean_text
from utils.ocr import ocr_page_bytes

def extract_pages_from_pdf_bytes(pdf_bytes: bytes, use_ocr_if_empty: bool = True) -> List[Dict]:
    pages = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            raw = page.extract_text() or ""
            text = clean_text(raw)
            if not text and use_ocr_if_empty:
                try:
                    text = clean_text(ocr_page_bytes(pdf_bytes, i))
                except Exception:
                    text = ""
            pages.append({"page_no": i, "text": text})
    return pages
