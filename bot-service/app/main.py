#Generate main
from fastapi import FastAPI
from app.routes.expense import router as expense_router
from app.routes.health import router as health_router
from app.core.db import init_db
app = FastAPI(
    title= "Darwin AI Bot Service",
    description= "API for managing expenses in the Darwin AI Bot Service",
    version= "1.0.0",
)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Include the expense router
app.include_router(expense_router)
app.include_router(health_router)
