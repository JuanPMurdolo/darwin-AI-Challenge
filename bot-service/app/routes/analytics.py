from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse, TaskStatusResponse
from app.tasks.analytics import run_analytics_task
from app.core.celery_worker import celery_app
from app.core.logging import get_logger
from celery.result import AsyncResult
from typing import Dict, Any

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=AnalyticsResponse)
async def create_analytics_task(analytic: AnalyticsRequest) -> AnalyticsResponse:
    """
    Create an asynchronous analytics task
    """
    try:
        logger.info("Creating analytics task", data=analytic.model_dump())
        # Submit task to Celery
        task = run_analytics_task.delay(analytic.model_dump())
        logger.info("Analytics task created", task_id=task.id)
        return AnalyticsResponse(
            task_id=task.id,
            status="PENDING"
        )
    except Exception as e:
        logger.error("Error creating analytics task", error=str(e))
        raise HTTPException(status_code=400, detail=f"Error creating task: {str(e)}")

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    Get the status of an analytics task
    """
    logger.info("Checking task status", task_id=task_id)
    
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state == "PENDING":
            return TaskStatusResponse(
                task_id=task_id,
                status="PENDING"
            )
        elif task_result.state == "SUCCESS":
            return TaskStatusResponse(
                task_id=task_id,
                status="SUCCESS",
                result=task_result.result
            )
        elif task_result.state == "FAILURE":
            logger.error("Task failed", task_id=task_id, error=str(task_result.result))
            return TaskStatusResponse(
                task_id=task_id,
                status="FAILED",
                error=str(task_result.result)
            )
        else:
            return TaskStatusResponse(
                task_id=task_id,
                status=task_result.state
            )
            
    except Exception as e:
        logger.error("Error checking task status", task_id=task_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Error checking task status: {str(e)}")

@router.get("/sync", response_model=Dict[str, Any])
async def get_analytics_sync(
    user_id: str,
    start_date: str = None,
    end_date: str = None
) -> Dict[str, Any]:
    """
    Get analytics synchronously (for testing purposes)
    """
    logger.info("Getting analytics synchronously", user_id=user_id, start_date=start_date, end_date=end_date)
    
    try:
        from datetime import datetime
        
        request_data = {"user_id": user_id}
        if start_date:
            request_data["start_date"] = datetime.fromisoformat(start_date).date()
        if end_date:
            request_data["end_date"] = datetime.fromisoformat(end_date).date()
            
        analytics_request = AnalyticsRequest(**request_data)
        service = AnalyticsService()
        result = await service.get_expense_analytics(analytics_request)
        
        return result.model_dump()
        
    except Exception as e:
        logger.error("Error in sync analytics", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")
