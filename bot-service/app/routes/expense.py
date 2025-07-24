
from app.services.expense import ExpenseService
from fastapi import APIRouter, Request
import logging
from app.schemas.expense import ExpenseInput

router = APIRouter(prefix="/expense", tags=["Expense"])
logger = logging.getLogger(__name__)

@router.post("/add")
async def add_expense(request: Request):
    data = await request.json()
    logger.info("Parsed raw data: %s", data)
    
    user_id = data.get("user_id")
    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")
    telegram_id = data.get("telegram_id")
    text = data.get("message") or data.get("text")  # compatibilidad

    expense_service = ExpenseService()
    return await expense_service.add_expense(
        user_id=user_id,
        description=description,
        amount=amount,
        category=category,
        telegram_id=telegram_id,
        text=text
    )
    
@router.get("/list")
async def get_expenses(request: Request):
    data = await request.json()
    user_id = data.get("user_id")

    expense_service = ExpenseService()
    return await expense_service.get_expenses(user_id)

@router.get("/{expense_id}")
async def get_expense_by_id(request: Request, expense_id: int):
    expense_service = ExpenseService()
    return await expense_service.get_expense_by_id(expense_id)

@router.delete("/{expense_id}")
async def delete_expense(request: Request, expense_id: int):
    expense_service = ExpenseService()
    return await expense_service.delete_expense(expense_id)

@router.put("/{expense_id}")
async def update_expense(request: Request, expense_id: int):
    data = await request.json()
    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")

    expense_service = ExpenseService()
    return await expense_service.update_expense(expense_id, description, amount, category)

@router.get("/analytics")
async def get_expense_analytics(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    expense_service = ExpenseService()
    return await expense_service.get_expense_analytics(user_id, start_date, end_date)
