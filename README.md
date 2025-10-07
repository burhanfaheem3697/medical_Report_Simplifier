# Medical Report Simplifier

A FastAPI-based service for extracting, structuring, normalizing, and summarizing medical report data from images. This project leverages OCR (Optical Character Recognition) and advanced text processing to make medical reports more accessible and understandable.

---

## 🚀 Features

- **OCR Extraction**: Extracts text from uploaded medical report images.
- **Structured Report**: Converts raw text into structured JSON data using LLM prompts.
- **Normalization**: Standardizes structured reports for consistency.
- **Summarization**: Generates patient-friendly summaries from normalized data.
- **Robust Error Handling**: Clean HTTP error responses for all endpoints.

---

## 📁 Project Structure

```
medicalReportSimplifier/
│
├── main.py                # FastAPI app & API endpoints
├── text_extractor.py      # OCR logic for extracting 
├── process_report.py      # Logic for structuring 
├── normalizer.py          # Functions for normalizing 
├── summarizer.py          # Patient-friendly summary 
├── schemas.py             # Pydantic models for request/
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```
---

## 🛠️ Installation

1. **Clone the repository**
    ```
    git clone https://github.com/yourusername/medicalReportSimplifier.git
    cd medicalReportSimplifier
    ```

2. **Create and activate a virtual environment**
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Install Tesseract OCR**
    - Download and install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
    - Make sure to update the path in `text_extractor.py` if needed:
      ```python
      pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
      ```

5. **Run the server**
    ```
    uvicorn main:app --reload --port 8000
    ```

---

## 📚 API Endpoints

### 1. Health Check

- **GET /**  
  Returns a simple hello world message.

---

### 2. OCR Extraction

- **POST /ocr/extract-text**  
  Upload an image of a medical report to extract text.

  **Request:**  
  - `image_file`: Image file (PNG, JPG, etc.)

  **Response:**  
  ```json
  {
    "filename": "report.jpg",
    "text": "Extracted text from the image..."
  }
  ```

---

### 3. Structured Report

- **POST /get-structured-report**  
  Converts raw OCR text into a structured JSON report using an LLM.

  **Request:**  
  ```json
  {
    "text": "Raw OCR text..."
  }
  ```

  **Response:**  
  ```json
  {
    "patient": {...},
    "sample": {...},
    "lab": {...},
    "results": [
      {
        "parameter": "...",
        "value": ...,
        "unit": "...",
        "reference_range": {
          "low": ...,
          "high": ...
        }
      }
    ]
  }
  ```

---

### 4. Normalize Report

- **POST /normalize**  
  Normalizes a structured report for consistency.

  **Request:**  
  ```json
  {
    "patient_name": "...",
    "age": "...",
    "diagnosis": "...",
    // other fields
  }
  ```

  **Response:**  
  ```json
  {
    "normalized_patient_name": "...",
    // normalized fields
  }
  ```

---

### 5. Summarize Report

- **POST /summarize-report**  
  Generates a patient-friendly summary from normalized report data.

  **Request:**  
  ```json
  {
    // normalized report fields
  }
  ```

  **Response:**  
  ```json
  {
    "summary": "Patient-friendly summary..."
  }
  ```

---

## 🧠 Prompts Used & Refinements Made

### LLM Prompt for Structuring Reports

The following system prompt is used in `process_report.py` to guide the LLM in converting raw medical report text into structured JSON:

```
You are a precision data extraction AI. Your task is to analyze raw text from a medical lab report and convert it into a structured JSON object.

The JSON object must contain 'patient', 'sample', 'lab', 'results'. 
The 'results' key must be a list of objects, each with 'parameter', 'value', 'unit', 'reference_range'.

**CRITICAL INSTRUCTION:** The 'reference_range' key MUST be a JSON object.
- For a range like "13.0-17.0", the object should be { "low": 13.0, "high": 17.0 }. 
- For a range like "<50", the object should be { "high": 50 }.
- For a range like ">4000", the object should be { "low": 4000 }.

For example, the text "Hemoglobin: 12.5 g/dL (Ref: 13.0-17.0) LOW" must be converted to:
{
"parameter": "Hemoglobin",
"value": 12.5,
"unit": "g/dL",
"reference_range": {
    "low": 13.0,
    "high": 17.0
}
}

```

**Refinements Made:**
- Enforced strict JSON output (no explanations or markdown).
- Added explicit instructions for handling reference ranges.
- Provided concrete examples for clarity.

---

## ⚠️ Known Issues & Potential Improvements

- **LLM Output Validation**: Occasionally, the LLM may return malformed JSON or include extra text. Additional validation and error handling may be needed.
- **Reference Range Parsing**: Complex or ambiguous reference ranges may not be parsed correctly by the LLM.
- **OCR Accuracy**: The quality of extracted text depends on image clarity and Tesseract configuration.
- **Environment Variables**: Ensure `.env` is properly configured for API keys and sensitive data.
- **Performance**: Large images or lengthy reports may slow down processing; consider optimizing or batching requests.
- **Extensibility**: Future improvements could include support for more report formats, additional languages, or enhanced summarization logic.

---


## 💡 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

For questions or support, please open an issue on GitHub.
