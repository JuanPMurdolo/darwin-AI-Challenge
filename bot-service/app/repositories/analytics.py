from sqlalchemy import func, select
from app.core.db import async_session
from app.models.expense import Expense
from datetime import date
from app.core.db import AsyncSessionLocal


class AnalyticsRepository:
    async def get_expenses_summary(self, user_id: int, start_date: date, end_date: date):
        async with AsyncSessionLocal() as session:
            query = (
                select(Expense.category, func.sum(Expense.amount).label("total"))
                .where(
                    Expense.user_id == user_id,
                    Expense.added_at >= start_date,
                    Expense.added_at <= end_date
                )
                .group_by(Expense.category)
            )
            result = await session.execute(query)
            return result.all()

    async def get_total_expenses(self, user_id: int, start_date: date, end_date: date):
        async with AsyncSessionLocal() as session:
            query = (
                select(func.sum(Expense.amount))
                .where(
                    Expense.user_id == user_id,
                    Expense.added_at >= start_date,
                    Expense.added_at <= end_date
                )
            )
            result = await session.execute(query)
            return result.scalar()
