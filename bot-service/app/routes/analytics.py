from fastapi import APIRouter, HTTPException, Query, Request
from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse
from app.tasks.analytics import run_analytics_task
import logging
from app.core.celery_worker import celery_app
from celery.result import AsyncResult


router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)

@router.post("/")
async def get_expense_analytics(request: Request):
    data = await request.json()
    task = run_analytics_task.delay(data)
    return {"task_id": task.id}

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.state == "PENDING":
        return {"status": "Pending"}
    elif task_result.state == "SUCCESS":
        return {"status": "Success", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "Failed", "error": str(task_result.result)}
    else:
        return {"status": task_result.state}