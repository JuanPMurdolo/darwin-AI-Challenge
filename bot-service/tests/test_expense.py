import pytest
from app.repositories.expense import ExpenseRepository
from app.models.expense import Expense
from datetime import datetime

class TestExpenseRepository:
    """Unit tests for expense repository"""
    
    @pytest.mark.asyncio
    async def test_add_expense_success(self, test_user):
        """Test successful expense addition"""
        repo = ExpenseRepository()
        
        result = await repo.add_expense(
            user_id=1,
            description="Test expense",
            amount=25.50,
            category="Food",
            telegram_id=test_user.telegram_id,
            text="Pizza 25.50"
        )
        
        assert result["status"] == "success"
        assert "expense added" in result["message"]

    @pytest.mark.asyncio
    async def test_add_expense_unauthorized(self):
        """Test expense addition with unauthorized user"""
        repo = ExpenseRepository()
        
        result = await repo.add_expense(
            user_id=1,
            description="Test expense",
            amount=25.50,
            category="Food",
            telegram_id="unauthorized_user",
            text="Pizza 25.50"
        )
        
        assert result["message"] == "Unauthorized"
