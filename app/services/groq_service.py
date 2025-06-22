from groq import Groq
from app.config import settings
from app.utils.exceptions import GroqAPIError
import json
import logging

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    async def generate_mcqs(self, prompt: str) -> dict:
        """Generate MCQs using Groq API"""
        try:
            logger.info("Sending request to Groq API")
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator and question generator. Always respond with valid JSON format as requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=settings.GROQ_MODEL,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            logger.info("Successfully received response from Groq API")
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise GroqAPIError("Failed to parse AI response")
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise GroqAPIError(f"Failed to generate questions: {str(e)}")
    
    async def test_connection(self) -> bool:
        """Test connection to Groq API"""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=settings.GROQ_MODEL,
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.error(f"Groq API connection test failed: {str(e)}")
            return False

# Global instance
groq_service = GroqService()