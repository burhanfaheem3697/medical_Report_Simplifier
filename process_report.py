# process_report.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_structured_report(raw_text: str):
    """
    Sends raw medical report text to the Groq API to get structured JSON.
    """
    try:
        # 1. Configure the API Client
        # The client automatically reads the GROQ_API_KEY from your .env file
        client = Groq()

        # 2. Engineer the Prompt
        # This prompt instructs the model on its role, the task, the required output format, and what to avoid.
        system_prompt = """
        You are an expert data extraction AI. Your task is to analyze the provided raw text from a medical lab report and convert it into a structured JSON object.

        The JSON object must contain the following keys: 'patient', 'sample', 'lab', 'results', and 'interpretation'. The 'results' key must be a list of objects, where each object has 'parameter', 'value', 'unit', 'reference_range', and 'flag' keys.

        Respond ONLY with the valid JSON object. Do not include any other text, explanations, or markdown formatting like ```json.
        """

        # 3. Call the Groq API
        print("Sending request to Groq API...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"Here is the medical report text:\n\n{raw_text}",
                },
            ],
            model="llama3-8b-8192",
            # This is a crucial parameter to ensure the output is a valid JSON object
            response_format={"type": "json_object"},
            temperature=0.0, # Set to 0 for deterministic, fact-based output
        )
        
        # 4. Return the Response
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Main execution block ---
# if __name__ == "__main__":
#     # This is the sample raw text from a medical report
#     raw_medical_text = """
#     DRLOGY PATHOLOGY LAB
#     105 -108, SMART VISION COMPLEX, HEALTHCARE ROAD, OPPOSITE HEALTHCARE COMPLEX. MUMBAI - 689578
#     Patient Name: Yash M. Patel (21/Male) - PID: 555
#     Ref by: Dr. Hiren Shah
#     Sample Type: Blood
#     Collected at: 125, Shivam Bungalow, S G Road, Mumbai on 02/12/202X 15:11
#     Reported on: 02/12/202X 16:35

#     Investigation: Complete Blood Count (CBC) with ESR
#     -----------------------------------------------------
#     Hemoglobin: 12.5 g/dL (Ref: 13.0-17.0) LOW
#     Packed Cell Volume (PCV): 57.5 % (Ref: <50) HIGH
#     RBC Count: 5.2 mill/cumm (Ref: 4.5-5.5)
#     Total WBC Count: 9000 cumm (Ref: 4000-11000)
#     Platelet Count: 150000 cumm (Ref: 150000-410000) BORDERLINE
#     -----------------------------------------------------
#     Interpretation: Further confirm for Anemia
#     """
    
#     structured_json_output = get_structured_report(raw_medical_text)
    
#     if structured_json_output:
#         print("\n--- Structured JSON Response ---")
#         print(structured_json_output)