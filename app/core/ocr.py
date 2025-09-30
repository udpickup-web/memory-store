import pytesseract
from PIL import Image

def ocr_image(img) -> str:
    return pytesseract.image_to_string(img, lang="rus+eng", config="--psm 6")
