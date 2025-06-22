class MCQGeneratorException(Exception):
    """Base exception for MCQ Generator"""
    pass

class GroqAPIError(MCQGeneratorException):
    """Exception raised for Groq API errors"""
    pass

class PDFProcessingError(MCQGeneratorException):
    """Exception raised for PDF processing errors"""
    pass

class ValidationError(MCQGeneratorException):
    """Exception raised for validation errors"""
    pass

class ConfigurationError(MCQGeneratorException):
    """Exception raised for configuration errors"""
    pass