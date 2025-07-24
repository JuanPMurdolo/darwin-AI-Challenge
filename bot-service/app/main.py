from fastapi import FastAPI
from app.routes.expense import router as expense_router
from app.routes.health import router as health_router
from app.routes.analytics import router as analytics_router
from app.core.db import init_db
from app.core.logging import configure_logging, get_logger
from app.core.config import LOG_LEVEL, ENVIRONMENT
import uvicorn

# Configure logging
configure_logging(LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(
    title="Darwin AI Bot Service",
    description="API for managing expenses in the Darwin AI Bot Service",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Darwin AI Bot Service", environment=ENVIRONMENT)
    await init_db()
    logger.info("Database initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Darwin AI Bot Service")

# Include routers
app.include_router(expense_router)
app.include_router(health_router)
app.include_router(analytics_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=ENVIRONMENT == "development",
        log_level=LOG_LEVEL.lower()
    )
