from fastapi import APIRouter, HTTPException
from app.core.logging import get_logger
from app.core.db import AsyncSessionLocal
from app.core.celery_worker import celery_app
from sqlalchemy import text
import redis
from app.core.config import REDIS_URL
from typing import Dict, Any

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint
    """
    logger.info("Health check requested")
    
    health_status = {
        "status": "healthy",
        "service": "bot-service",
        "checks": {
            "database": "unknown",
            "redis": "unknown",
            "celery": "unknown"
        }
    }
    
    # Check database connection
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        health_status["checks"]["database"] = "healthy"
        logger.info("Database health check passed")
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
        logger.error("Database health check failed", error=str(e))
    
    # Check Redis connection
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
        health_status["checks"]["redis"] = "healthy"
        logger.info("Redis health check passed")
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
        logger.error("Redis health check failed", error=str(e))
    
    # Check Celery workers
    try:
        inspect = celery_app.control.inspect()
        active_workers = inspect.active()
        if active_workers:
            health_status["checks"]["celery"] = f"healthy: {len(active_workers)} workers"
        else:
            health_status["checks"]["celery"] = "unhealthy: no active workers"
            health_status["status"] = "degraded"
        logger.info("Celery health check completed", active_workers=len(active_workers) if active_workers else 0)
    except Exception as e:
        health_status["checks"]["celery"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
        logger.error("Celery health check failed", error=str(e))
    
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status

@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check for Kubernetes/Docker
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        raise HTTPException(status_code=503, detail={"status": "not ready", "error": str(e)})

@router.get("/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for Kubernetes/Docker
    """
    return {"status": "alive"}
