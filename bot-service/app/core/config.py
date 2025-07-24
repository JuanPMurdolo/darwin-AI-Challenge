import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# AI/ML
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")

# Celery/Redis
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
