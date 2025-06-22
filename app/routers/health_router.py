from fastapi import APIRouter, HTTPException
from app.models.request_models import HealthCheckResponse
from app.services.groq_service import groq_service
from app.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health Check"])

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint with Groq API connectivity test"""
    try:
        # Test Groq API connectivity
        groq_status = "connected" if await groq_service.test_connection() else "disconnected"
        
        return HealthCheckResponse(
            status="healthy" if groq_status == "connected" else "degraded",
            timestamp=datetime.now().isoformat(),
            groq_api=groq_status,
            version=settings.APP_VERSION
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/ready")
async def readiness_check():
    """Readiness check for deployment"""
    return {"status": "ready", "timestamp": datetime.now().isoformat()}

@router.get("/live")
async def liveness_check():
    """Liveness check for deployment"""
    return {"status": "alive", "timestamp": datetime.now().isoformat()}