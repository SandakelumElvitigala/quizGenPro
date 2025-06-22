from pydantic import BaseModel, Field, validator
from typing import Optional
from app.config import settings

class TopicRequest(BaseModel):
    topic: str = Field(..., description="Topic to generate MCQs about", min_length=3)
    num_questions: int = Field(
        default=settings.DEFAULT_QUESTIONS, 
        ge=settings.MIN_QUESTIONS, 
        le=settings.MAX_QUESTIONS,
        description="Number of questions to generate"
    )
    difficulty: str = Field(
        default="medium", 
        description="Difficulty level: easy, medium, hard"
    )
    question_type: str = Field(
        default="general", 
        description="Type of questions: general, analytical, factual"
    )
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v not in settings.DIFFICULTY_LEVELS:
            raise ValueError(f'Difficulty must be one of: {settings.DIFFICULTY_LEVELS}')
        return v
    
    @validator('question_type')
    def validate_question_type(cls, v):
        if v not in settings.QUESTION_TYPES:
            raise ValueError(f'Question type must be one of: {settings.QUESTION_TYPES}')
        return v

class PDFRequest(BaseModel):
    num_questions: int = Field(
        default=settings.DEFAULT_QUESTIONS,
        ge=settings.MIN_QUESTIONS,
        le=settings.MAX_QUESTIONS,
        description="Number of questions to generate"
    )
    difficulty: str = Field(
        default="medium",
        description="Difficulty level: easy, medium, hard"
    )
    question_type: str = Field(
        default="general",
        description="Type of questions: general, analytical, factual"
    )
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v not in settings.DIFFICULTY_LEVELS:
            raise ValueError(f'Difficulty must be one of: {settings.DIFFICULTY_LEVELS}')
        return v
    
    @validator('question_type')
    def validate_question_type(cls, v):
        if v not in settings.QUESTION_TYPES:
            raise ValueError(f'Question type must be one of: {settings.QUESTION_TYPES}')
        return v

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    groq_api: str
    version: str