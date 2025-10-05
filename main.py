# main.py
import pytesseract
import io
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from typing import Annotated
from text_extractor import extract_text_from_image
from process_report import get_structured_report
import uvicorn
app = FastAPI(
    title="Medical Report OCR Service",
    description="Extracts text from a medical report image."
)


@app.get('/')
def hell():
    return {"message" : "helloworld"}

@app.post("/ocr/extract-text", tags=["OCR"])
async def extract_text_from_image(
    image_file: Annotated[UploadFile, File(description="An image of a medical report.")]
):
    return await extract_text_from_image(image_file)

@app.get('/get-structured/report')
async def structured_report(raw_medical_text):
    return await get_structured_report(raw_medical_text)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)