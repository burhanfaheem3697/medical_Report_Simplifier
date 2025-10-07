# services.py
import json
from groq import AsyncGroq
from schemas import StructuredReport # Assuming your Pydantic model is imported

def create_unified_summary_prompt(report_data) -> str:
    """
    Creates a single, powerful prompt that asks the LLM to both identify
    significant results from the full report and then summarize them.
    """
    prompt = """
    You are a helpful AI assistant that explains medical lab results to a patient in simple, non-alarming terms.
    Your task is to analyze the following list of medical test results and the lab's overall interpretation.
    First, you must internally identify which of these results are clinically significant or abnormal (e.g., any result that is outside its reference range, or any qualitative result that is 'Detected', 'Positive', 'Reactive', or otherwise noteworthy).
    Then, based ONLY on these significant findings, generate a brief 'summary' and a list of 'explanations'.
    If all results are normal, state that clearly in the summary and provide an empty list for explanations.
    
    CRITICAL: Do not provide a diagnosis, medical advice, or recommendations. Do not use alarming language.

    Here are the test results:
    """
    # Serialize the list of tests into a clean string format for the prompt
    for test in report_data.results:
        prompt += f"- {test.parameter}: {test.value} {test.unit or ''}\n"

    # Provide the lab's own interpretation for extra context if it exists
    # if report_data.interpretation:
    #     prompt += f"\nLab's Interpretation for Context: '{report_data.interpretation}'"
        
    prompt += "\n\nRespond ONLY with a valid JSON object with 'summary' (a string) and 'explanations' (a list of objects, each with 'finding' and 'explanation' keys)."
    return prompt

async def get_patient_summary(data):
    """
    Generates a patient-friendly summary from a full, structured report.
    """
    if not data.results:
        return {"summary": "The report contains no test results to summarize.", "explanations": []}

    prompt = create_unified_summary_prompt(data)
    client = AsyncGroq()
    
    chat_completion = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="openai/gpt-oss-120b",
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    
    response_content = chat_completion.choices[0].message.content
    return json.loads(response_content)