
from app.services.expense import ExpenseService
from fastapi import APIRouter, Request
import logging
from app.schemas.expense import ExpenseInput

router = APIRouter(prefix="/expense", tags=["Expense"])
logger = logging.getLogger(__name__)

@router.post("/add")
async def add_expense(data: ExpenseInput):
    logger.info("Parsed data: %s", data.model_dump())
    
    expense_service = ExpenseService()
    return await expense_service.add_expense(
        user_id=data.user_id,
        description=data.description,
        amount=data.amount,
        category=data.category,
        telegram_id=data.telegram_id,
        text=data.text
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