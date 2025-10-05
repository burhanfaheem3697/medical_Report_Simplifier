import json
from groq import AsyncGroq
from schemas import Report  # Assuming your Pydantic model is imported

# ---------------------------------------------------------------------------
# 1. The new, robust filtering logic
# ---------------------------------------------------------------------------
def filter_abnormal_results(data):
    """
    Robustly filters the list of tests to find abnormal results
    by comparing the value to the reference range.
    """
    abnormal = []
    for test in data.results:
        # Skip if value or reference range is missing
        if test.value is None or not test.reference_range:
            continue

        is_abnormal = False
        low = test.reference_range.get("low")
        high = test.reference_range.get("high")

        if low is not None and test.value < low:
            is_abnormal = True
        
        if high is not None and test.value > high:
            is_abnormal = True

        if is_abnormal:
            abnormal.append(test)
            
    return abnormal

# ---------------------------------------------------------------------------
# 2. The new, more effective prompt
# ---------------------------------------------------------------------------
def create_llm_prompt(abnormal_results) -> str:
    """Creates a more detailed and effective prompt for the LLM."""
    prompt = """
    You are a helpful AI assistant that explains medical lab results to a patient in simple, non-alarming terms.
    Your tone should be helpful and informative, but not clinical.
    **CRITICAL: Do not provide a diagnosis, medical advice, or any recommendations. Do not use alarming language.**

    Based on the following findings from a blood report, generate a brief 'summary' and a list of 'explanations'.
    For each explanation, identify the status (e.g., 'Low', 'High') in the 'finding' field and provide a simple, one-sentence explanation.
    
    Findings:
    """
    for result in abnormal_results:
        # Provide more context to the LLM (value, units, and the normal range)
        range_str = f"Normal: {result.reference_range.get('low', 'N/A')} - {result.reference_range.get('high', 'N/A')}"
        prompt += f"- Parameter: {result.parameter}, Patient's Value: {result.value} {result.unit}, ({range_str})\n"
        
    prompt += "\nRespond ONLY with a valid JSON object with two keys: 'summary' (a string) and 'explanations' (a list of objects, each with 'finding' and 'explanation' keys)."
    return prompt

# ---------------------------------------------------------------------------
# 3. The main service function (updated with the new model name)
# ---------------------------------------------------------------------------
async def get_patient_summary(data):
    """Generates a patient-friendly summary from normalized test data."""
    print("hello1")
    abnormal_results = filter_abnormal_results(data)
    print("hello2")
    if not abnormal_results:
        return {
            "summary": "All test results appear to be within the normal range.",
            "explanations": []
        }
    
    prompt = create_llm_prompt(abnormal_results)
    client = AsyncGroq()
    
    chat_completion = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="openai/gpt-oss-120b",  # Using the updated, more powerful model
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    
    response_content = chat_completion.choices[0].message.content
    print("hello3")
    return json.loads(response_content)