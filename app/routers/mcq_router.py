from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from app.models.request_models import TopicRequest, PDFRequest
from app.models.response_models import MCQResponse, ErrorResponse
from app.services.mcq_service import mcq_service
from app.services.pdf_service import pdf_service
from app.utils.exceptions import PDFProcessingError, GroqAPIError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/generate", tags=["MCQ Generation"])

@router.post("/topic", response_model=MCQResponse)
async def generate_mcqs_from_topic(request: TopicRequest):
    """Generate MCQs from a given topic"""
    try:
        response = await mcq_service.generate_mcqs_from_topic(
            topic=request.topic,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            question_type=request.question_type
        )
        logger.info(response)
        return response
        
    except GroqAPIError as e:
        logger.error(f"Groq API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/pdf", response_model=MCQResponse)
async def generate_mcqs_from_pdf(
    file: UploadFile = File(...),
    request: PDFRequest = Depends()  # Use PDFRequest model
):
    """Generate MCQs from uploaded PDF file"""
    try:
        # Validate file
        pdf_service.validate_pdf_file(file.filename, file.size or 0)
        
        # Read and extract text from PDF
        file_content = await file.read()
        text_content = pdf_service.extract_text_from_pdf(file_content)
        
        # Generate MCQs
        response = await mcq_service.generate_mcqs_from_pdf(
            pdf_content=text_content,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            question_type=request.question_type
        )
        logger.info(request.num_questions)
        return response
        
    except PDFProcessingError as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except GroqAPIError as e:
        logger.error(f"Groq API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")