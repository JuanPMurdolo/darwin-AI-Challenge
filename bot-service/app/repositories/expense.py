from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.expense import Expense
from app.handlers.langchain_handler import categorize_expense
from sqlalchemy import select
from datetime import datetime

class ExpenseRepository:
    def __init__(self):
        pass

    async def add_expense(self, user_id: int, description: str, amount: float, category: str, telegram_id: str, text: str):
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(User).where(User.telegram_id == telegram_id))
                user = result.scalar_one_or_none()
                print("Lookig for user with telegram_id:", telegram_id)

                if not user:
                    print("❌ User not found")
                    return None
                print("User found:", user)
                print("Text to categorize", text)
                parsed = await categorize_expense(text)
                if not parsed or len(parsed) != 3:
                    return None
                print("Parsed expense:", parsed)
                category, amount, description = parsed

                expense = Expense(
                    user_id=user.id,
                    description=description,
                    amount=amount,
                    category=category,
                    added_at=datetime.utcnow()
                )

                session.add(expense)
                print("Expense added:", expense)
                await session.commit()
                print("Expense committed to DB")
                await session.refresh(expense)
                # Attach telegram_id for response serialization
                expense.telegram_id = user.telegram_id
                return expense

        except Exception as e:
            import traceback
            traceback.print_exc()
            return None
        
    async def get_expenses(self, user_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return {"message": "Unauthorized"}

            expenses = await session.execute(select(Expense).where(Expense.user_id == user.id))
            return expenses.scalars().all()
        
    async def get_expense_by_id(self, expense_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Expense).where(Expense.id == expense_id))
            expense = result.scalar_one_or_none()

            if not expense:
                return {"message": "Expense not found"}

            return expense
        
    async def delete_expense(self, expense_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Expense).where(Expense.id == expense_id))
            expense = result.scalar_one_or_none()

            if not expense:
                return {"message": "Expense not found"}

            await session.delete(expense)
            await session.commit()
            return {"message": "Expense deleted successfully"}
        
    async def update_expense(self, expense_id: int, description: str = None, amount: float = None, category: str = None):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Expense).where(Expense.id == expense_id))
            expense = result.scalar_one_or_none()

            if not expense:
                return {"message": "Expense not found"}

            if description:
                expense.description = description
            if amount:
                expense.amount = amount
            if category:
                expense.category = category

            await session.commit()
            return {"message": "Expense updated successfully"}
        
    async def get_expense_analytics(self, user_id: int, start_date: str, end_date: str):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return {"message": "Unauthorized"}

            query = select(Expense).where(
                Expense.user_id == user.id,
                Expense.added_at >= start_date,
                Expense.added_at <= end_date
            )
            expenses = await session.execute(query)
            total_expenses = expenses.scalars().all()
            total_amount = sum(expense.amount for expense in total_expenses)
            media_amount_per_category = total_amount / len(set(expense.category for expense in total_expenses)) if total_expenses else 0
            variation_percentage = 0
            if len(total_expenses) > 1:
                first_month_expense = total_expenses[0].amount
                last_month_expense = total_expenses[-1].amount
                if first_month_expense != 0:
                    variation_percentage = ((last_month_expense - first_month_expense) / first_month_expense) * 100
            
            return {
                "total_amount": total_amount,
                "media_amount_per_category": media_amount_per_category,
                "variation_percentage": variation_percentage
            }
