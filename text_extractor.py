from fastapi import UploadFile, File
from typing import Annotated
import pytesseract
import io
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

async def extract_text_from_image(
    image_file: Annotated[UploadFile, File(description="An image of a medical report.")]
):
    """
    Receives an image, performs OCR using Tesseract, and returns the extracted text.
    """
    file_contents = await image_file.read()
    try:
        image = Image.open(io.BytesIO(file_contents))
    except Exception as e:
        return {"error": f"Failed to open image: {e}"}
    try:
        extracted_text = pytesseract.image_to_string(image)
        return {
            "filename": image_file.filename,
            "text": extracted_text
        }
    except Exception as e:
        return {"error": f"Failed during OCR processing: {e}"}