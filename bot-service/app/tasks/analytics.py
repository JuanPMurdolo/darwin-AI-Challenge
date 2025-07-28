from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsRequest
from app.core.celery_worker import celery_app
from app.core.logging import get_logger
import asyncio
from typing import Dict, Any

logger = get_logger(__name__)

@celery_app.task(name="run_analytics_task", bind=True)
def run_analytics_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Celery task to run analytics asynchronously
    """
    task_id = self.request.id
    logger.info("Starting analytics task", task_id=task_id, payload=payload)
    
    try:
        service = AnalyticsService()
        request = AnalyticsRequest(**payload)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(service.get_expense_analytics(request))
            result_dict = result.model_dump()
            
            logger.info("Analytics task completed successfully", task_id=task_id)
            return result_dict
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Analytics task failed", task_id=task_id, error=str(e))
        raise self.retry(exc=e, countdown=60, max_retries=3)
