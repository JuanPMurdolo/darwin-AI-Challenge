from fastapi import APIRouter, HTTPException, Query, Request
from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse
from celery.result import AsyncResult
import logging


router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)

@router.post("/")
async def get_expense_analytics(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    logger.info(f"Received analytics request: user_id={user_id}, start_date={start_date}, end_date={end_date}")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    if not start_date or not end_date:
        raise HTTPException(status_code=400, detail="Start date and end date are required")
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")
    if not isinstance(start_date, str) or not isinstance(end_date, str):
        raise HTTPException(status_code=400, detail="Start date and end date must be strings in ISO format")
    
    logger.info("Validating dates and user ID")
    
    request_data = AnalyticsRequest(
    user_id=user_id,
    start_date=start_date,
    end_date=end_date
    )
    
    logger.info(f"Request data for analytics: {request_data}")

    analytics_service = AnalyticsService()
    logger.info("Calling AnalyticsService to get expense analytics")
    return await analytics_service.get_expense_analytics(request_data)