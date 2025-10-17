# ocr_utils.py
import pytesseract
from PIL import Image

def ocr_image_pil(pil_image: Image.Image) -> str:
    # optionally convert to grayscale/resize for better OCR
    gray = pil_image.convert("L")
    text = pytesseract.image_to_string(gray)
    return text
