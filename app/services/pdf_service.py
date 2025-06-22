import PyPDF2
import io
from app.config import settings
from app.utils.exceptions import PDFProcessingError
import logging

logger = logging.getLogger(__name__)

class PDFService:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text content from PDF file"""
        try:
            logger.info("Starting PDF text extraction")
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    text += page_text + "\n"
                    logger.debug(f"Extracted text from page {page_num + 1}")
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1}: {str(e)}")
                    continue
            
            text = text.strip()
            
            if not text:
                raise PDFProcessingError("No text could be extracted from the PDF")
            
            if len(text) < 50:
                raise PDFProcessingError("PDF content is too short to generate meaningful questions")
            
            # Truncate if too long
            if len(text) > settings.MAX_PDF_CHARS:
                text = text[:settings.MAX_PDF_CHARS] + "..."
                logger.info(f"PDF content truncated to {settings.MAX_PDF_CHARS} characters")
            
            logger.info(f"Successfully extracted {len(text)} characters from PDF")
            return text
            
        except PDFProcessingError:
            raise
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise PDFProcessingError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def validate_pdf_file(filename: str, file_size: int) -> None:
        """Validate PDF file before processing"""
        if not filename.lower().endswith('.pdf'):
            raise PDFProcessingError("Only PDF files are supported")
        
        if file_size > settings.MAX_FILE_SIZE:
            raise PDFProcessingError(f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE} bytes")

# Global instance
pdf_service = PDFService()