from pydantic import BaseModel
from typing import Dict,Any,List

class ResultItem(BaseModel):
    parameter: str
    value: float | None
    unit: str | None
    reference_range: Dict[str, Any] | None
    status: str | None

class Report(BaseModel):
    results: List[ResultItem]
    # You can add other fields like 'patient', 'lab', etc. if you need them.

class OcrOutput(BaseModel):
    filename: str
    text: str

class PatientInfo(BaseModel):
    name: str
    age: int
    sex: str

class SampleInfo(BaseModel):
    collected_at: str | None
    collected_on: str | None
    reported_on: str | None

class LabInfo(BaseModel):
    name: str
    address: str | None
    instrument: str | None
    report_generated_on: str | None

# This is the main model that represents the entire JSON object
# This is what your normalizer route will take as input.
class StructuredReport(BaseModel):
    patient: PatientInfo
    sample: SampleInfo
    lab: LabInfo
    results: List[ResultItem]
    interpretation: str