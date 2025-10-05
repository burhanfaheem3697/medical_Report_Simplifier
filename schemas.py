from pydantic import BaseModel

class ResultItem(BaseModel):
    parameter: str
    value: float | None
    unit: str | None
    flag: str | None
    reference_range: Dict[str, Any] | None

class Report(BaseModel):
    results: List[ResultItem]
    # You can add other fields like 'patient', 'lab', etc. if you need them.

class DetailedReport(BaseModel):
    report: Report

class OcrOutput(BaseModel):
    filename: str
    text: str