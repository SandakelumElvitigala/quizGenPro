from pydantic import BaseModel
from typing import List, Optional

class MCQOption(BaseModel):
    option: str
    is_correct: bool

class MCQuestion(BaseModel):
    question: str
    options: List[MCQOption]
    explanation: str

class MCQResponse(BaseModel):
    questions: List[MCQuestion]
    generated_at: str
    source_type: str
    topic: Optional[str] = None
    total_questions: int
    metadata: Optional[dict] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None

class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None