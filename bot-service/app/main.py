#Generate main
from fastapi import FastAPI
from app.routes.expense import router as expense_router
from app.core.config import settings
from app.core.db import init_db, create_admin
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    await create_admin()  # Ensure admin user is created on startup


# Include the expense router
app.include_router(expense_router)
