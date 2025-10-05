from fastapi import UploadFile, File
from typing import Annotated
import pytesseract
import io
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def extract_text_from_image(file_contents: bytes) -> str:
    """
    Performs OCR on the given image bytes using Tesseract.
    Raises errors if the file is not a valid image or if Tesseract fails.
    """
    # This line will raise an UnidentifiedImageError if the file is not a valid image.
    image = Image.open(io.BytesIO(file_contents))
    
    # This line will raise an error if Tesseract is not configured correctly.
    extracted_text = pytesseract.image_to_string(image)
    
    return extracted_text