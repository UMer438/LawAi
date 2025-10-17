# pdf_utils.py
from io import BytesIO
import PyPDF2

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        texts = []
        for page in reader.pages:
            try:
                texts.append(page.extract_text() or "")
            except Exception:
                texts.append("")
        return "\n\n".join(texts)
    except Exception as e:
        return f"[PDF extraction failed: {e}]"
