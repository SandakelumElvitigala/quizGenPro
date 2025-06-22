from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "MCQ Generator AI Agent"
    APP_DESCRIPTION: str = "Generate multiple choice questions from PDF documents or topics using Groq API"
    APP_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7
    
    # File Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_PDF_CHARS: int = 8000
    ALLOWED_FILE_TYPES: List[str] = [".pdf"]
    
    # MCQ Configuration
    MIN_QUESTIONS: int = 1
    MAX_QUESTIONS: int = 20
    DEFAULT_QUESTIONS: int = 5
    DIFFICULTY_LEVELS: List[str] = ["easy", "medium", "hard"]
    QUESTION_TYPES: List[str] = ["general", "analytical", "factual"]
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()