import pytest
from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsRequest
from datetime import date
from decimal import Decimal

class TestAnalyticsService:
    """Unit tests for analytics calculations"""
    
    @pytest.mark.asyncio
    async def test_total_expenses_calculation(self, test_user, test_expenses):
        """Test total expenses calculation"""
        service = AnalyticsService()
        
        request = AnalyticsRequest(
            user_id=test_user.id,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )
        
        result = await service.get_expense_analytics(request)
        
        # Should include expenses from January (25.50 + 15.00 = 40.50)
        assert result.total_expenses == 40.50
        assert len(result.category_breakdown) == 2
        
        # Check category breakdown
        food_category = next((c for c in result.category_breakdown if c.category == "Food"), None)
        transport_category = next((c for c in result.category_breakdown if c.category == "Transportation"), None)
        
        assert food_category is not None
        assert food_category.total == 25.50
        assert transport_category is not None
        assert transport_category.total == 15.00

    @pytest.mark.asyncio
    async def test_category_average_calculation(self, test_user, test_expenses):
        """Test average calculation by category"""
        service = AnalyticsService()
        
        request = AnalyticsRequest(
            user_id=test_user.id,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 2, 28)
        )
        
        result = await service.get_expense_analytics(request)
        
        # Food category should have average of (25.50 + 30.00) / 2 = 27.75
        assert "Food" in result.average_by_category
        assert result.average_by_category["Food"] == 27.75
        
        # Transportation should have average of 15.00
        assert "Transportation" in result.average_by_category
        assert result.average_by_category["Transportation"] == 15.00

    @pytest.mark.asyncio
    async def test_empty_date_range(self, test_user):
        """Test analytics with no expenses in date range"""
        service = AnalyticsService()
        
        request = AnalyticsRequest(
            user_id=test_user.id,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        )
        
        result = await service.get_expense_analytics(request)
        
        assert result.total_expenses == 0.0
        assert len(result.category_breakdown) == 0
        assert len(result.average_by_category) == 0

    @pytest.mark.asyncio
    async def test_nonexistent_user(self):
        """Test analytics for non-existent user"""
        service = AnalyticsService()
        
        request = AnalyticsRequest(
            user_id="nonexistent_user",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )
        
        result = await service.get_expense_analytics(request)
        
        assert result.total_expenses == 0.0
        assert len(result.category_breakdown) == 0
