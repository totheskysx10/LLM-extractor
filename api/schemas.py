from typing import List, Optional
from pydantic import BaseModel


class LearnExample(BaseModel):
    value: str
    ocr_json: str


class LearnRequest(BaseModel):
    document_type: str
    field_name: str
    examples: List[LearnExample]
    force: bool = False


class LearnJobResponse(BaseModel):
    job_id: str


class PredictRequest(BaseModel):
    document_type: str
    field_name: str
    ocr_json: str


class JobResponse(BaseModel):
    job_id: str


class JobResultResponse(BaseModel):
    status: str
    value: Optional[str] = None
    error: Optional[str] = None