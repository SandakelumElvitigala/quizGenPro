#!/usr/bin/env python3
"""
Server startup script for MCQ Generator API
"""
import uvicorn
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings

def main():
    """Start the server"""
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Server will be available at: http://{settings.HOST}:{settings.PORT}")
    print(f"API docs will be available at: http://{settings.HOST}:{settings.PORT}/docs")
    
    # Check if Groq API key is set
    if not settings.GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY is not set. Please set it in your environment or .env file")
        sys.exit(1)
    
    port = int(os.environ.get("PORT", settings.PORT))
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=port,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )

if __name__ == "__main__":
    main()