from fastapi import UploadFile, File
from typing import Annotated
import pytesseract
import io
from PIL import Image
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"



def extract_text_from_image(file_contents: bytes) -> str:
    """
    Extracts text from an uploaded image using Tesseract OCR.
    This version uses a specific Page Segmentation Mode (PSM) for better
    accuracy on single-column medical reports, removing complex pre-processing.
    """
    # First, read the file's content into a bytes object.
    # image_bytes = await file_upload.read()

    try:
        image = Image.open(io.BytesIO(file_contents))

        # Use Page Segmentation Mode 4: "Assume a single column of text of variable sizes."
        # This is often more reliable for report-style documents than the complex
        # contour detection logic, which can fail on clear, single-column images.
        custom_config = r'--oem 3 --psm 4'
        text = pytesseract.image_to_string(image, config=custom_config)

        return text
    except Exception as e:
        raise IOError(f"Tesseract OCR failed to process the image. Error: {e}")