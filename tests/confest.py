import pytest
import os
import sys
from unittest.mock import Mock

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def mock_groq_response():
    """Mock Groq API response"""
    return {
        "questions": [
            {
                "question": "What is Python?",
                "options": [
                    {"option": "A) A snake", "is_correct": False},
                    {"option": "B) A programming language", "is_correct": True},
                    {"option": "C) A framework", "is_correct": False},
                    {"option": "D) A database", "is_correct": False}
                ],
                "explanation": "Python is a high-level programming language."
            }
        ]
    }

@pytest.fixture
def sample_pdf_content():
    """Sample PDF text content"""
    return """
    Introduction to Machine Learning
    
    Machine learning is a subset of artificial intelligence that enables computers
    to learn and improve from experience without being explicitly programmed.
    
    There are three main types of machine learning:
    1. Supervised Learning
    2. Unsupervised Learning  
    3. Reinforcement Learning
    
    Supervised learning uses labeled data to train models that can make predictions
    on new, unseen data.
    """

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment"""
    # Set test environment variables
    os.environ.setdefault("GROQ_API_KEY", "test-key")
    os.environ.setdefault("LOG_LEVEL", "ERROR")  # Reduce log noise in tests