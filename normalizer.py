from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any



# --- 1. The Normalization Logic (remains simple) ---
# This function only runs if the Pydantic validation above succeeds.
def normalize_json(validated_data):
    normalized_tests = []
    for result in validated_data.results:
        if result.value is not None:
            normalized_tests.append({
                "parameter": result.parameter,
                "value": result.value,
                "unit": result.unit,
                "reference_range": result.reference_range,
                "status": result.status
            })
    return {"results": normalized_tests, "normalization_confidence": 0.95}


