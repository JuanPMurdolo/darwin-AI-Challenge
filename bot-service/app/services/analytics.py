from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import AnalyticsRequest, AnalyticsResult, CategoryBreakdown
from datetime import date


class AnalyticsService:
    def __init__(self):
        self.repo = AnalyticsRepository()

    async def run_analytics(self, data: AnalyticsRequest):
        start_date = data.start_date or date.min
        end_date = data.end_date or date.max

        category_data = await self.repo.get_expenses_summary(data.user_id, start_date, end_date)
        category_breakdown = [
            CategoryBreakdown(category=row[0], total=row[1]) for row in category_data
        ]

        total_expenses = await self.repo.get_total_expenses(data.user_id, start_date, end_date)

        return AnalyticsResult(
            total_expenses=total_expenses or 0.0,
            start_date=start_date,
            end_date=end_date,
            category_breakdown=category_breakdown
        )
