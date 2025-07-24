from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsRequest
from app.core.celery_worker import celery_app
from fastapi.concurrency import run_in_threadpool


@celery_app.task(name="run_analytics_task")
def run_analytics_task(payload: dict):
    import asyncio

    service = AnalyticsService()
    request = AnalyticsRequest(**payload)

    # Usar loop de asyncio porque el servicio es async
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(service.get_expense_analytics(request)).model_dump()