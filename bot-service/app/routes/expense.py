from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_db
from app.core.logging import get_logger
from app.services.expense import ExpenseService
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all expenses with pagination"""
    try:
        logger.info("Fetching expenses", skip=skip, limit=limit)
        service = ExpenseService()
        expenses = await service.get_expenses(skip=skip, limit=limit)
        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    expense: ExpenseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new expense"""
    try:
        logger.info("Creating expense", data=expense.model_dump())
        service = ExpenseService()
        return await service.create_expense(expense)
    except Exception as e:
        logger.error("Error creating expense", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific expense by ID"""
    try:
        logger.info("Fetching expense by ID", expense_id=expense_id)
        service = ExpenseService()
        expense = await service.get_expense(expense_id)
        if not expense:
            logger.warning("Expense not found", expense_id=expense_id)
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense
    except HTTPException:
        logger.error("Error fetching expense", expense_id=expense_id)
        raise
    except Exception as e:
        logger.error("Unexpected error fetching expense", expense_id=expense_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing expense"""
    try:
        logger.info("Updating expense", expense_id=expense_id, data=expense_update.model_dump())
        service = ExpenseService()
        expense = await service.update_expense(expense_id, expense_update)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense
    except HTTPException:
        logger.error("Error updating expense", expense_id=expense_id)
        raise
    except Exception as e:
        logger.error("Unexpected error updating expense", expense_id=expense_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an expense"""
    try:
        logger.info("Deleting expense", expense_id=expense_id)
        service = ExpenseService()
        success = await service.delete_expense(expense_id)
        if not success:
            raise HTTPException(status_code=404, detail="Expense not found")
        return {"message": "Expense deleted successfully"}
    except HTTPException:
        logger.error("Error deleting expense", expense_id=expense_id)
        raise
    except Exception as e:
        logger.error("Unexpected error deleting expense", expense_id=expense_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
