import pytest
from app.services.analytics import AnalyticsService
from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import AnalyticsRequest
from datetime import date, datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta

class TestAnalyticsRepository:
    """Unit tests for analytics repository"""

    @pytest.mark.asyncio
    async def test_get_expenses_summary(self, test_user, test_expenses):
        """Test getting expenses summary by category"""
        repo = AnalyticsRepository()
        
        result = await repo.get_expenses_summary(
            test_user.id, 
            date(2024, 1, 1), 
            date(2024, 1, 31)
        )
        
        # Should have 2 categories in January
        assert len(result) == 2
        
        # Convert to dict for easier testing
        summary_dict = {row[0]: float(row[1]) for row in result}
        assert summary_dict["Food"] == 25.50
        assert summary_dict["Transportation"] == 15.00

    @pytest.mark.asyncio
    async def test_get_expenses_summary_empty_range(self, test_user, test_expenses):
        """Test getting expenses summary for empty date range"""
        repo = AnalyticsRepository()
        
        result = await repo.get_expenses_summary(
            test_user.id, 
            date(2023, 1, 1), 
            date(2023, 12, 31)
        )
        
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_total_expenses(self, test_user, test_expenses):
        """Test getting total expenses"""
        repo = AnalyticsRepository()
        
        total = await repo.get_total_expenses(
            test_user.id, 
            date(2024, 1, 1), 
            date(2024, 1, 31)
        )
        
        assert float(total) == 40.50  # 25.50 + 15.00

    @pytest.mark.asyncio
    async def test_get_total_expenses_no_data(self, test_user):
        """Test getting total expenses with no data"""
        repo = AnalyticsRepository()
        
        total = await repo.get_total_expenses(
            test_user.id, 
            date(2023, 1, 1), 
            date(2023, 12, 31)
        )
        
        assert total is None

    @pytest.mark.asyncio
    async def test_get_average_by_category(self, test_user, test_expenses):
        """Test getting average by category"""
        repo = AnalyticsRepository()
        
        result = await repo.get_average_by_category(
            test_user.id, 
            date(2024, 1, 1), 
            date(2024, 2, 28)
        )
        
        # Convert to dict for easier testing
        avg_dict = {row[0]: float(row[1]) for row in result}
        
        # Food category: (25.50 + 30.00) / 2 = 27.75
        assert avg_dict["Food"] == 27.75
        # Transportation: 15.00 / 1 = 15.00
        assert avg_dict["Transportation"] == 15.00

    @pytest.mark.asyncio
    async def test_get_monthly_variation_increase(self, test_user):
        """Test monthly variation calculation with increase"""
        repo = AnalyticsRepository()
        
        # Mock the get_total_expenses method for this test
        from unittest.mock import AsyncMock, patch
        
        with patch.object(repo, 'get_total_expenses') as mock_get_total:
            # Current month: 100, Previous month: 80
            mock_get_total.side_effect = [Decimal('100'), Decimal('80')]
            
            variation = await repo.get_monthly_variation(
                test_user.id,
                date(2024, 2, 1),
                date(2024, 1, 1)
            )
            
            # (100 - 80) / 80 * 100 = 25%
            assert variation == 25.0

    @pytest.mark.asyncio
    async def test_get_monthly_variation_no_previous_data(self, test_user):
        """Test monthly variation with no previous data"""
        repo = AnalyticsRepository()
        
        from unittest.mock import AsyncMock, patch
        
        with patch.object(repo, 'get_total_expenses') as mock_get_total:
            # Current month: 100, Previous month: None
            mock_get_total.side_effect = [Decimal('100'), None]
            
            variation = await repo.get_monthly_variation(
                test_user.id,
                date(2024, 2, 1),
                date(2024, 1, 1)
            )
            
            assert variation == 0.0


class TestAnalyticsService:
    """Unit tests for analytics service"""

    @pytest.mark.asyncio
    async def test_get_expense_analytics_full_data(self, test_user, test_expenses):
        """Test getting complete analytics"""
        service = AnalyticsService()
        
        request = AnalyticsRequest(
            user_id=test_user.id,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )
        
        result = await service.get_expense_analytics(request)
        
        # Check total expenses
        assert result.total_expenses == 40.50
        
        # Check category breakdown
        assert len(result.category_breakdown) == 2
        categories = {cb.category: cb.total for cb in result.category_breakdown}
        assert categories["Food"] == 25.50
        assert categories["Transportation"] == 15.00
        
        # Check date range
        assert result.start_date == date(2024, 1, 1)
        assert result.end_date == date(2024, 1, 31)

    @pytest.mark.asyncio
    async def test_get_expense_analytics_all_time(self, test_user, test_expenses):
        """Test analytics without date range (all time)"""
        service = AnalyticsService()
        
        request = AnalyticsRequest(user_id=test_user.id)
        
        result = await service.get_expense_analytics(request)
        
        # Should include all expenses: 25.50 + 15.00 + 30.00 = 70.50
        assert result.total_expenses == 70.50
        assert len(result.category_breakdown) == 2
        
        # Check averages
        assert "Food" in result.average_by_category
        assert "Transportation" in result.average_by_category
        # Food average: (25.50 + 30.00) / 2 = 27.75
        assert result.average_by_category["Food"] == 27.75

    @pytest.mark.asyncio
    async def test_get_expense_analytics_empty_result(self, test_user):
        """Test analytics with no expenses in range"""
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
    async def test_get_expense_analytics_nonexistent_user(self, db_session):
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

    @pytest.mark.asyncio
    async def test_get_expense_analytics_invalid_date_range(self, test_user):
        """Test analytics with invalid date range"""
        service = AnalyticsService()
        
        request = AnalyticsRequest(
            user_id=test_user.id,
            start_date=date(2024, 12, 31),  # Start after end
            end_date=date(2024, 1, 1)
        )
        
        with pytest.raises(ValueError, match="start_date debe ser anterior"):
            await service.get_expense_analytics(request)

    @pytest.mark.asyncio
    async def test_get_expense_analytics_with_monthly_variation(self, test_user, test_expenses):
        """Test analytics with monthly variation calculation"""
        service = AnalyticsService()
        
        # Mock the monthly variation calculation
        from unittest.mock import patch
        
        with patch.object(service.repo, 'get_monthly_variation', return_value=15.5):
            request = AnalyticsRequest(
                user_id=test_user.id,
                start_date=date(2024, 2, 1),
                end_date=date(2024, 2, 28)
            )
            
            result = await service.get_expense_analytics(request)
            
            assert result.monthly_variation_percentage == 15.5

    @pytest.mark.asyncio
    async def test_get_expense_analytics_monthly_variation_error(self, test_user, test_expenses):
        """Test analytics when monthly variation calculation fails"""
        service = AnalyticsService()
        
        # Mock the monthly variation to raise an exception
        from unittest.mock import patch
        
        with patch.object(service.repo, 'get_monthly_variation', side_effect=Exception("DB Error")):
            request = AnalyticsRequest(
                user_id=test_user.id,
                start_date=date(2024, 2, 1),
                end_date=date(2024, 2, 28)
            )
            
            result = await service.get_expense_analytics(request)
            
            # Should default to 0.0 when calculation fails
            assert result.monthly_variation_percentage == 0.0
