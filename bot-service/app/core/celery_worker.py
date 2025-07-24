from celery import Celery
from app.core.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from app.core.logging import get_logger

logger = get_logger(__name__)

celery_app = Celery(
    "expense_bot",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['app.tasks.analytics']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

logger.info("Celery app configured", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
