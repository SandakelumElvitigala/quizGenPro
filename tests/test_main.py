import pytest
from fastapi.testclient import TestClient
from app.main import app
import json
import os

client = TestClient(app)

class TestMain:
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        # May fail if GROQ_API_KEY is not set
        assert response.status_code in [200, 503]

    def test_ready_endpoint(self):
        """Test readiness endpoint"""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_live_endpoint(self):
        """Test liveness endpoint"""
        response = client.get("/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    @pytest.mark.skipif(not os.getenv("GROQ_API_KEY"), reason="GROQ_API_KEY not set")
    def test_generate_from_topic(self):
        """Test MCQ generation from topic"""
        payload = {
            "topic": "Python Programming",
            "num_questions": 2,
            "difficulty": "easy",
            "question_type": "general"
        }
        
        response = client.post("/api/v1/generate/topic", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "questions" in data
        assert len(data["questions"]) <= 2
        assert data["source_type"] == "topic"

    def test_generate_from_topic_validation(self):
        """Test validation for topic generation"""
        # Test with empty topic
        payload = {
            "topic": "",
            "num_questions": 1
        }
        
        response = client.post("/api/v1/generate/topic", json=payload)
        assert response.status_code == 422

        # Test with invalid difficulty
        payload = {
            "topic": "Test topic",
            "difficulty": "invalid"
        }
        
        response = client.post("/api/v1/generate/topic", json=payload)
        assert response.status_code == 422

    def test_generate_from_pdf_no_file(self):
        """Test PDF generation without file"""
        response = client.post("/api/v1/generate/pdf")
        assert response.status_code == 422

    def test_generate_from_pdf_invalid_file(self):
        """Test PDF generation with invalid file"""
        files = {"file": ("test.txt", b"Some text content", "text/plain")}
        
        response = client.post("/api/v1/generate/pdf", files=files)
        assert response.status_code == 400