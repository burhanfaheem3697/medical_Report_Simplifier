# main.py
import pytesseract
from fastapi import FastAPI, UploadFile, File,HTTPException,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Annotated
from text_extractor import extract_text_from_image
from process_report import get_structured_report
from normalizer import normalize_json
from schemas import OcrOutput,Report,StructuredReport
from summarizer import get_patient_summary
import uvicorn
app = FastAPI(
    title="Medical Report OCR Service",
    description="Extracts text from a medical report image."
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # ADD THIS LINE to see the detailed error in your terminal
    print(f"Caught a validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={"message": "An error occurred with your input.", "details": exc.errors()},
    )


@app.get('/')
def hell():
    return {"message" : "helloworld"}

@app.post("/ocr/extract-text", tags=["OCR"])
async def extract_text(
    image_file: Annotated[UploadFile, File(description="An image of a medical report.")]
):
    """
    Receives an image file and returns the extracted text.
    Handles all errors and communicates them via HTTPExceptions.
    """

    try:
        # First, read the file contents from the upload
        file_contents = await image_file.read()
        
        # Then, call the service to do the processing
        extracted_text = extract_text_from_image(file_contents)
        
        # If successful, return the result
        return {
            "filename": image_file.filename,
            "text": extracted_text
        }
    except UnidentifiedImageError:
        # Catch the specific error for bad image files
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a valid image."
        )
    except Exception as e:
        # Catch any other unexpected errors from the service
        print(f"An unexpected OCR error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred during OCR processing."
        )


@app.post('/get-structured-report')
async def structured_report(request: OcrOutput):
    """
    Receives raw text in a POST request and returns a structured JSON report.
    This is the "front desk" that handles errors gracefully.
    """
    try:
        # Call the service to perform the main task
        structured_data = await get_structured_report(request.text)
        print("printing structured data",structured_data)
        return structured_data  
    except Exception as e:
        # Catch any error from the service and return a clean HTTP error response
        print(f"An error occurred in the service layer: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal server error occurred while processing the report."
        )

@app.post("/normalize")
async def normalize_report(structured_report : Report):
    """
    Receives a detailed report, which is automatically validated by FastAPI/Pydantic.
    If validation passes, it proceeds to normalize it.
    """
    try:
        normalized_data = normalize_json(structured_report)
        return normalized_data
    except Exception as e:
        # This will catch errors in your normalization logic
        raise HTTPException(status_code=500, detail=f"Error during normalization: {str(e)}")

@app.post("/summarize-report")
async def summarize_report_endpoint(request : Report):
    """
    Receives a full structured report and returns a patient-friendly summary.
    This endpoint delegates the task of identifying what's important to the LLM.
    """
    try:
        # Call the single, unified summarization service
        summary_data = await get_patient_summary(request)
        return summary_data
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the summary: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)