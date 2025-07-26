from sqlalchemy import func, select, extract
from app.models.expense import Expense
from datetime import date, datetime
from app.core.db import get_new_async_session
from app.core.logging import get_logger
from typing import List, Tuple, Optional
from decimal import Decimal

logger = get_logger(__name__)

class AnalyticsRepository:
    async def get_expenses_summary(self, user_id: str, start_date: date, end_date: date) -> List[Tuple[str, Decimal]]:
        """Get expense summary by category for a user within date range"""
        logger.info("Getting expenses summary", user_id=user_id, start_date=start_date, end_date=end_date)
        
        try:
            AsyncSessionLocal = get_new_async_session()
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
                data = result.all()
                
                logger.info("Expenses summary retrieved", categories_count=len(data))
                return data
                
        except Exception as e:
            logger.error("Error getting expenses summary", error=str(e), user_id=user_id)
            raise

    async def get_total_expenses(self, user_id: str, start_date: date, end_date: date) -> Optional[Decimal]:
        """Get total expenses for a user within date range"""
        logger.info("Getting total expenses", user_id=user_id, start_date=start_date, end_date=end_date)
        
        try:
            AsyncSessionLocal = get_new_async_session()
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
                total = result.scalar()
                
                logger.info("Total expenses retrieved", total=float(total) if total else 0)
                return total
                
        except Exception as e:
            logger.error("Error getting total expenses", error=str(e), user_id=user_id)
            raise

    async def get_monthly_variation(self, user_id: str, current_month: date, previous_month: date) -> float:
        """Calculate monthly variation percentage"""
        logger.info("Calculating monthly variation", user_id=user_id, current_month=current_month, previous_month=previous_month)
        
        try:
            # Get current month total
            current_total = await self.get_total_expenses(user_id, current_month, current_month.replace(day=28))
            
            # Get previous month total  
            prev_total = await self.get_total_expenses(user_id, previous_month, previous_month.replace(day=28))
            
            if not prev_total or prev_total == 0:
                logger.info("No previous month data for variation calculation")
                return 0.0
                
            if not current_total:
                current_total = Decimal('0')
                
            variation = float(((current_total - prev_total) / prev_total) * 100)
            
            logger.info("Monthly variation calculated", variation=variation)
            return variation
            
        except Exception as e:
            logger.error("Error calculating monthly variation", error=str(e), user_id=user_id)
            raise

    async def get_average_by_category(self, user_id: str, start_date: date, end_date: date) -> List[Tuple[str, Decimal]]:
        """Get average expense amount by category"""
        logger.info("Getting average by category", user_id=user_id, start_date=start_date, end_date=end_date)
        
        try:
            AsyncSessionLocal = get_new_async_session()
            async with AsyncSessionLocal() as session:
                query = (
                    select(
                        Expense.category, 
                        func.avg(Expense.amount).label("average")
                    )
                    .where(
                        Expense.user_id == user_id,
                        Expense.added_at >= start_date,
                        Expense.added_at <= end_date
                    )
                    .group_by(Expense.category)
                )
                result = await session.execute(query)
                data = result.all()
                
                logger.info("Average by category retrieved", categories_count=len(data))
                return data
                
        except Exception as e:
            logger.error("Error getting average by category", error=str(e), user_id=user_id)
            raise
