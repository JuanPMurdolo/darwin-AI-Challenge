from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import AnalyticsRequest, AnalyticsResult, CategoryBreakdown
from app.core.logging import get_logger
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from typing import List

logger = get_logger(__name__)

class AnalyticsService:
    def __init__(self):
        self.repo = AnalyticsRepository()

    async def get_expense_analytics(self, data: AnalyticsRequest) -> AnalyticsResult:
        """Generate comprehensive expense analytics"""
        logger.info("Starting expense analytics", user_id=data.user_id, start_date=data.start_date, end_date=data.end_date)
        
        try:
            # Validación de rango de fechas
            if data.start_date and data.end_date:
                if data.start_date > data.end_date:
                    raise ValueError("start_date debe ser anterior o igual a end_date.")
            start_date = data.start_date or date.min
            end_date = data.end_date or date.max

            # Get category breakdown
            category_data = await self.repo.get_expenses_summary(data.user_id, start_date, end_date)
            category_breakdown = [
                CategoryBreakdown(category=row[0], total=float(row[1])) for row in category_data
            ]

            # Get total expenses
            total_expenses = await self.repo.get_total_expenses(data.user_id, start_date, end_date)
            total_expenses_float = float(total_expenses) if total_expenses else 0.0

            # Get average by category
            avg_data = await self.repo.get_average_by_category(data.user_id, start_date, end_date)
            avg_by_category = {row[0]: float(row[1]) for row in avg_data}

            # Calculate monthly variation if we have date range
            monthly_variation = 0.0
            if data.start_date and data.end_date:
                try:
                    current_month = data.end_date.replace(day=1)
                    previous_month = current_month - relativedelta(months=1)
                    monthly_variation = await self.repo.get_monthly_variation(
                        data.user_id, current_month, previous_month
                    )
                except Exception as e:
                    logger.warning("Could not calculate monthly variation", error=str(e))

            result = AnalyticsResult(
                total_expenses=total_expenses_float,
                start_date=start_date,
                end_date=end_date,
                category_breakdown=category_breakdown,
                average_by_category=avg_by_category,
                monthly_variation_percentage=monthly_variation
            )

            logger.info("Analytics completed successfully", 
                       total_expenses=total_expenses_float,
                       categories_count=len(category_breakdown),
                       monthly_variation=monthly_variation)
            
            return result

        except Exception as e:
            logger.error("Error in expense analytics", error=str(e), user_id=data.user_id)
            raise
