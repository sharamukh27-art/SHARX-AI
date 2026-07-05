"""System and health check endpoints"""

from fastapi import APIRouter, HTTPException
import psutil
from app.ai.factory import get_current_provider
from app.utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        provider = get_current_provider()
        is_healthy = await provider.health_check()
        
        return {
            "status": "healthy" if is_healthy else "degraded",
            "provider": provider.model_name,
            "provider_available": is_healthy
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_system_stats():
    """Get system statistics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        return {
            "cpu_percent": cpu_percent,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            }
        }
    except Exception as e:
        logger.error(f"Error fetching system stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_app_info():
    """Get application information"""
    try:
        provider = get_current_provider()
        return {
            "app_name": "SHAR-X AI",
            "version": "1.0.0",
            "ai_provider": provider.model_name,
            "description": "The Future of Intelligent Assistance"
        }
    except Exception as e:
        logger.error(f"Error fetching app info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
