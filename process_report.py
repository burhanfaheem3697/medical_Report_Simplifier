# process_report.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def get_structured_report(raw_text):
    """
    Sends raw medical report text to the Groq API to get structured JSON.
    If an API error occurs, it will be raised and caught by the route handler.
    """
    client = AsyncGroq()
    
    system_prompt = """
    You are an expert data extraction AI. Your task is to analyze the provided raw text from a medical lab report and convert it into a structured JSON object.
    The JSON object must contain 'patient', 'sample', 'lab', 'results', and 'interpretation'. The 'results' key must be a list of objects, each with 'parameter', 'value', 'unit', 'reference_range', and 'flag' keys.
    Respond ONLY with the valid JSON object. Do not include any other text, explanations, or markdown formatting.
    """
    
    print("Sending request to Groq API...")
    chat_completion = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the medical report text:\n\n{raw_text}"},
        ],
        model="llama3-8b-8192",
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    
    # The response from the LLM is a JSON string, so we parse it into a Python dict
    response_content = chat_completion.choices[0].message.content
    return json.loads(response_content)