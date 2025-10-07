# process_report.py
import os
from groq import AsyncGroq
from dotenv import load_dotenv
import json
# Load environment variables from .env file
load_dotenv()

async def get_structured_report(raw_text):
    """
    Sends raw medical report text to the Groq API to get structured JSON.
    If an API error occurs, it will be raised and caught by the route handler.
    """
    client = AsyncGroq()
    
    system_prompt = """
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

    Respond ONLY with the valid JSON object. Do not include any other text, explanations, or markdown formatting.
    """
    
    print("Sending request to Groq API...")
    chat_completion = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the medical report text:\n\n{raw_text}"},
        ],
        model="openai/gpt-oss-120b",
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    
    # The response from the LLM is a JSON string, so we parse it into a Python dict
    response_content = chat_completion.choices[0].message.content
    return json.loads(response_content)