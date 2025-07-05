


from app.core.db import AsyncSessionLocal, async_session
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
                    return {"message": "Unauthorized"}
                print("User found:", user)
                
                # Check if the user exists
                # if not user:
                print("Text to categorize", text)
                parsed = await categorize_expense(text)
                if not parsed or len(parsed) != 3:
                    return {"message": "Not an expense"}
                
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
                return {"message": f"{category} expense added ✅", "status": "success"}

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"message": f"Error adding expense: {str(e)}"}
        
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
        