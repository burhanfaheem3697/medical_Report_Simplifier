from fastapi import FastAPI, HTTPException
from schemas import DetailedReport
from typing import List, Dict, Any



# --- 1. The Normalization Logic (remains simple) ---
# This function only runs if the Pydantic validation above succeeds.
def normalize_json(validated_data):
    normalized_tests = []
    for result in validated_data.report.results:
        if result.value is not None:
            normalized_tests.append({
                "name": result.parameter,
                "value": result.value,
                "unit": result.unit,
                "status": result.flag,
                "ref_range": result.reference_range
            })
    return {"tests": normalized_tests, "normalization_confidence": 0.95}


