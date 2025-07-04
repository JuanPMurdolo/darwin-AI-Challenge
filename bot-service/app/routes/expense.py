
from app.services.expense import ExpenseService
from fastapi import APIRouter, Request
import logging

router = APIRouter(prefix="/expense", tags=["Expense"])
logger = logging.getLogger(__name__)

@router.post("/add")
async def add_expense(request: Request):
    data = await request.json()
    logger.info("Adding expense with data: %s", data)
    user_id = data.get("user_id")
    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")
    telegram_id = data.get("telegram_id")
    text = data.get("text")
    logger.info("Parsed data: user_id=%s, description=%s, amount=%s, category=%s, telegram_id=%s, text=%s",
                user_id, description, amount, category, telegram_id, text)

    expense_service = ExpenseService()
    logger.info("Calling add_expense service with user_id: %s", user_id)
    return await expense_service.add_expense(user_id, description, amount, category, telegram_id, text)
    
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