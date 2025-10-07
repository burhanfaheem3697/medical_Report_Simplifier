# Medical Report Simplifier

A FastAPI-based service for extracting, structuring, normalizing, and summarizing medical report data from images. This project leverages OCR (Optical Character Recognition) and advanced text processing to make medical reports more accessible and understandable.

---

## 🚀 Features

- **OCR Extraction**: Extracts text from uploaded medical report images.
- **Structured Report**: Converts raw text into structured JSON data.
- **Normalization**: Standardizes structured reports for consistency.
- **Summarization**: Generates patient-friendly summaries from normalized data.
- **Robust Error Handling**: Clean HTTP error responses for all endpoints.

---

## 📁 Project Structure

```
medicalReportSimplifier/
│
├── main.py                # FastAPI app & API endpoints
├── text_extractor.py      # OCR logic for extracting text from images
├── process_report.py      # Logic for structuring extracted text
├── normalizer.py          # Functions for normalizing structured reports
├── summarizer.py          # Patient-friendly summary generation
├── schemas.py             # Pydantic models for request/response validation
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
  Converts raw OCR text into a structured JSON report.

  **Request:**  
  ```json
  {
    "text": "Raw OCR text..."
  }
  ```

  **Response:**  
  ```json
  {
    "patient_name": "...",
    "age": "...",
    "diagnosis": "...",
    // other structured fields
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



## 💡 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

For questions or support, please open an issue on GitHub.
