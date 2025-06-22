from app.services.groq_service import groq_service
from app.models.response_models import MCQuestion, MCQOption, MCQResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MCQService:
    @staticmethod
    def create_mcq_prompt(content: str, num_questions: int, difficulty: str, question_type: str, is_pdf: bool = False) -> str:
        """Create prompt for Groq API to generate MCQs"""
        source_context = "based on the following PDF content" if is_pdf else "about the following topic"
        
        difficulty_instructions = {
            "easy": "Create simple, straightforward questions that test basic understanding and recall.",
            "medium": "Create moderate difficulty questions that require some analysis and comprehension.",
            "hard": "Create challenging questions that require deep understanding, analysis, and critical thinking."
        }
        
        type_instructions = {
            "general": "Mix different types of questions including factual, conceptual, and application-based.",
            "analytical": "Focus on questions that require analysis, comparison, evaluation, and critical thinking.",
            "factual": "Focus on questions that test specific facts, definitions, and direct information recall."
        }
        
        prompt = f"""
You are an expert educator and question generator. Create {num_questions} high-quality multiple choice questions {source_context}.

Content/Topic: {content}

Instructions:
- Difficulty: {difficulty} - {difficulty_instructions.get(difficulty, '')}
- Question Type: {question_type} - {type_instructions.get(question_type, '')}
- Each question must have exactly 4 options (A, B, C, D)
- Only one option should be correct
- Provide clear, educational explanations for the correct answers
- Questions should be diverse and cover different aspects of the content
- Avoid ambiguous, trick, or poorly constructed questions
- Ensure questions are grammatically correct and professionally written
- Make sure all options are plausible but only one is definitively correct

Return the response in the following JSON format:
{{
    "questions": [
        {{
            "question": "Question text here?",
            "options": [
                {{"option": "A) Option text", "is_correct": false}},
                {{"option": "B) Option text", "is_correct": true}},
                {{"option": "C) Option text", "is_correct": false}},
                {{"option": "D) Option text", "is_correct": false}}
            ],
            "explanation": "Detailed explanation why the correct answer is correct and why other options are incorrect"
        }}
    ]
}}

IMPORTANT: Return only valid JSON, no additional text or formatting.
"""
        return prompt
    
    @staticmethod
    async def generate_mcqs_from_topic(topic: str, num_questions: int, difficulty: str, question_type: str) -> MCQResponse:
        """Generate MCQs from a topic"""
        try:
            logger.info(f"Generating {num_questions} MCQs for topic: {topic}")
            
            prompt = MCQService.create_mcq_prompt(
                content=topic,
                num_questions=num_questions,
                difficulty=difficulty,
                question_type=question_type,
                is_pdf=False
            )
            
            result = await groq_service.generate_mcqs(prompt)
            
            questions = []
            for q_data in result.get("questions", []):
                options = [MCQOption(**opt) for opt in q_data["options"]]
                question = MCQuestion(
                    question=q_data["question"],
                    options=options,
                    explanation=q_data["explanation"]
                )
                questions.append(question)
            
            response = MCQResponse(
                questions=questions,
                generated_at=datetime.now().isoformat(),
                source_type="topic",
                topic=topic,
                total_questions=len(questions),
                metadata={
                    "difficulty": difficulty,
                    "question_type": question_type,
                    "requested_questions": num_questions
                }
            )
            
            logger.info(f"Successfully generated {len(questions)} MCQs from topic")
            return response
            
        except Exception as e:
            logger.error(f"Error generating MCQs from topic: {str(e)}")
            raise
    
    @staticmethod
    async def generate_mcqs_from_pdf(pdf_content: str, num_questions: int, difficulty: str, question_type: str) -> MCQResponse:
        """Generate MCQs from PDF content"""
        try:
            logger.info(f"Generating {num_questions} MCQs from PDF content")
            
            prompt = MCQService.create_mcq_prompt(
                content=pdf_content,
                num_questions=num_questions,
                difficulty=difficulty,
                question_type=question_type,
                is_pdf=True
            )
            
            result = await groq_service.generate_mcqs(prompt)
            
            questions = []
            for q_data in result.get("questions", []):
                options = [MCQOption(**opt) for opt in q_data["options"]]
                question = MCQuestion(
                    question=q_data["question"],
                    options=options,
                    explanation=q_data["explanation"]
                )
                questions.append(question)
            
            response = MCQResponse(
                questions=questions,
                generated_at=datetime.now().isoformat(),
                source_type="pdf",
                total_questions=len(questions),
                metadata={
                    "difficulty": difficulty,
                    "question_type": question_type,
                    "requested_questions": num_questions,
                    "content_length": len(pdf_content)
                }
            )
            
            logger.info(f"Successfully generated {len(questions)} MCQs from PDF")
            return response
            
        except Exception as e:
            logger.error(f"Error generating MCQs from PDF: {str(e)}")
            raise

# Global instance
mcq_service = MCQService()