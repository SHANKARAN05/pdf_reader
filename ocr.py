import pdfplumber

def ocr_page_bytes(pdf_bytes: bytes, page_number: int):
    with pdfplumber.open(pdf_bytes) as pdf:
        page = pdf.pages[page_number - 1]
        return page.extract_text() or ""

def ocr_all_pages(pdf_bytes: bytes):
    texts = []
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return texts