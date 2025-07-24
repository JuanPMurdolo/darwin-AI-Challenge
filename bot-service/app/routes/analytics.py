from fastapi import APIRouter, HTTPException, Query, Request
from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse
from celery.result import AsyncResult


router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)

@router.get("/")
async def get_expense_analytics(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    analytics_service = AnalyticsService()
    return await analytics_service.get_expense_analytics(user_id, start_date, end_date)

@router.get("/status/{task_id}", response_model=AnalyticsResponse)
async def get_analytics_status(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == "PENDING":
        return AnalyticsResponse(status="PENDING")
    elif task_result.state == "SUCCESS":
        return AnalyticsResponse(status="SUCCESS", result=task_result.result)
    elif task_result.state == "FAILURE":
        return AnalyticsResponse(status="FAILURE", error=str(task_result.result))
    else:
        return AnalyticsResponse(status=task_result.state)