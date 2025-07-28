from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.expense import Expense
from app.handlers.langchain_handler import categorize_expense
from sqlalchemy import select
from datetime import datetime
from app.core.logging import get_logger

logger = get_logger(__name__)

class ExpenseRepository:
    def __init__(self):
        pass

    async def add_expense(self, user_id: int, description: str, amount: float, category: str, telegram_id: str, text: str):
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(User).where(User.telegram_id == telegram_id))
                user = result.scalar_one_or_none()
                logger.info("Looking for user with telegram_id:", telegram_id=telegram_id)
                if not user:
                    logger.info("❌ User not found, creating new user")
                    user = User(id=telegram_id, telegram_id=telegram_id)
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                logger.info("User found:", user=user.id, telegram_id=user.telegram_id)
                logger.info("Text to categorize", text=text)
                parsed = await categorize_expense(text)
                if not parsed or len(parsed) != 3:
                    return None
                logger.info("Parsed expense:", text=parsed)
                category, amount, description = parsed

                expense = Expense(
                    user_id=user.id,
                    description=description,
                    amount=amount,
                    category=category,
                    added_at=datetime.utcnow()
                )

                session.add(expense)
                logger.info("Committing expense to DB", expense=expense)
                await session.commit()
                logger.info("Expense committed to DB", expense=expense)
                await session.refresh(expense)
                expense.telegram_id = user.telegram_id
                return expense

        except Exception as e:
            import traceback
            traceback.print_exc()
            return None
        
    async def get_expenses(self, user_id: int, skip: int = 0, limit: int = 10):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                logger.warning("Unauthorized access attempt by user_id", user_id=user_id)
                return {"message": "Unauthorized"}

            query = select(Expense).where(Expense.user_id == user.id).offset(skip).limit(limit)
            expenses = await session.execute(query)
            return expenses.scalars().all()

    async def get_all_expenses(self, skip= 0, limit=100):
        async with AsyncSessionLocal() as session:
            logger.info("Fetching all expenses with skip:", skip, "and limit:", limit)
            query = select(Expense).offset(skip).limit(limit)
            expenses = await session.execute(query)
            return expenses.scalars().all()
        
    async def get_expense_by_id(self, expense_id: int):
        async with AsyncSessionLocal() as session:
            logger.info("Fetching expense by ID:", expense_id=expense_id)
            result = await session.execute(select(Expense).where(Expense.id == expense_id))
            expense = result.scalar_one_or_none()

            if not expense:
                return {"message": "Expense not found"}

            return expense
        
    async def delete_expense(self, expense_id: int):
        async with AsyncSessionLocal() as session:
            logger.info("Deleting expense with ID:", expense_id=expense_id)
            result = await session.execute(select(Expense).where(Expense.id == expense_id))
            expense = result.scalar_one_or_none()

            if not expense:
                logger.warning("Attempted to delete non-existent expense", expense_id=expense_id)
                return {"message": "Expense not found"}

            await session.delete(expense)
            logger.info("Expense deleted successfully", expense_id=expense_id)
            await session.commit()
            return {"message": "Expense deleted successfully"}
        
    async def update_expense(self, expense_id: int, description: str = None, amount: float = None, category: str = None):
        async with AsyncSessionLocal() as session:
            logger.info("Updating expense with ID:", expense_id=expense_id)
            result = await session.execute(select(Expense).where(Expense.id == expense_id))
            expense = result.scalar_one_or_none()

            if not expense:
                logger.warning("Attempted to update non-existent expense", expense_id=expense_id)
                return {"message": "Expense not found"}

            if description:
                expense.description = description
            if amount:
                expense.amount = amount
            if category:
                expense.category = category

            logger.info("Committing updated expense to DB", expense=expense)

            await session.commit()
            return {"message": "Expense updated successfully"}
        
    async def get_expense_analytics(self, user_id: int, start_date: str, end_date: str):
        async with AsyncSessionLocal() as session:
            logger.info("Fetching expense analytics for user_id:", user_id, "from", start_date, "to", end_date)
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                logger.warning("Unauthorized access attempt for analytics by user_id", user_id=user_id)
                return {"message": "Unauthorized"}

            query = select(Expense).where(
                Expense.user_id == user.id,
                Expense.added_at >= start_date,
                Expense.added_at <= end_date
            )
            logger.info("Executing query for expense analytics", query=query)
            expenses = await session.execute(query)
            total_expenses = expenses.scalars().all()
            if not total_expenses:
                logger.info("No expenses found for analytics", user_id=user_id)
                return {"message": "No expenses found"}
            total_amount = sum(expense.amount for expense in total_expenses)
            logger.info("Total amount calculated for analytics", total_amount=total_amount)
            media_amount_per_category = total_amount / len(set(expense.category for expense in total_expenses)) if total_expenses else 0
            
            variation_percentage = 0
            if len(total_expenses) > 1:
                first_month_expense = total_expenses[0].amount
                last_month_expense = total_expenses[-1].amount
                if first_month_expense != 0:
                    variation_percentage = ((last_month_expense - first_month_expense) / first_month_expense) * 100
            
            logger.info("Expense analytics calculated", total_amount=total_amount, media_amount_per_category=media_amount_per_category, variation_percentage=variation_percentage)
            return {
                "total_amount": total_amount,
                "media_amount_per_category": media_amount_per_category,
                "variation_percentage": variation_percentage
            }
