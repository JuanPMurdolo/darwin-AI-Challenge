import pytest
from app.repositories.expense import ExpenseRepository
from app.services.expense import ExpenseService
from app.schemas.expense import ExpenseCreate
from datetime import datetime
from decimal import Decimal

class TestExpenseRepository:
    """Unit tests for expense repository"""

    @pytest.mark.asyncio
    async def test_add_expense_success(self, test_user, mock_langchain_handler):
        """Test adding expense successfully"""
        repo = ExpenseRepository()
        
        result = await repo.add_expense(
            user_id="1",
            description="Pizza",
            amount=25.50,
            category="Food",
            telegram_id=test_user.telegram_id,
            text="Pizza 25.50"
        )
        
        assert result is not None
        assert result.amount == Decimal("25.50")
        assert result.telegram_id == test_user.telegram_id

    @pytest.mark.asyncio
    async def test_get_all_expenses(self, test_expenses):
        """Test getting all expenses"""
        repo = ExpenseRepository()
        
        expenses = await repo.get_all_expenses(skip=0, limit=10)
        
        assert len(expenses) == 3
        assert all(hasattr(expense, 'description') for expense in expenses)

    @pytest.mark.asyncio
    async def test_get_expense_by_id(self, test_expenses):
        """Test getting expense by ID"""
        repo = ExpenseRepository()
        expense_id = test_expenses[0].id
        expense = await repo.get_expense_by_id(expense_id)
        assert expense is not None
        assert expense["id"] == expense_id
        assert expense["description"] == "Test Food Expense"
        assert "telegram_id" in expense

    @pytest.mark.asyncio
    async def test_delete_expense(self, test_expenses):
        """Test deleting expense"""
        repo = ExpenseRepository()
        expense_id = test_expenses[0].id
        
        result = await repo.delete_expense(expense_id)
        
        assert isinstance(result, dict)
        assert result["message"] == "Expense deleted successfully"

    @pytest.mark.asyncio
    async def test_update_expense(self, test_expenses):
        """Test updating expense"""
        repo = ExpenseRepository()
        expense_id = test_expenses[0].id
        
        result = await repo.update_expense(
            expense_id, 
            description="Updated Food", 
            amount=30.00, 
            category="Food"
        )
        
        assert isinstance(result, dict)
        assert result["id"] == expense_id
        assert result["description"] == "Updated Food"
        assert result["amount"] == 30.00
        assert result["category"] == "Food"
        assert "telegram_id" in result


class TestExpenseService:
    """Unit tests for expense service"""

    @pytest.mark.asyncio
    async def test_create_expense_success(self, test_user, mock_langchain_handler):
        """Test creating expense via service"""
        service = ExpenseService()
        
        expense_data = ExpenseCreate(
            user_id="1",
            description="Pizza",
            amount=25.50,
            category="Food",
            telegram_id=test_user.telegram_id,
            text="Pizza 25.50"
        )
        
        result = await service.create_expense(expense_data)
        
        assert result is not None
        assert result.amount == Decimal("25.50")

    @pytest.mark.asyncio
    async def test_create_expense_missing_fields(self):
        """Test creating expense with missing fields"""
        service = ExpenseService()
        
        class IncompleteExpenseData:
            user_id = None
            description = "Pizza"
            amount = 25.50
            category = "Food"
            telegram_id = "123456789"
            text = "Pizza 25.50"
        
        expense_data = IncompleteExpenseData()
        
        with pytest.raises(ValueError, match="All fields are required"):
            await service.create_expense(expense_data)

    @pytest.mark.asyncio
    async def test_get_expenses(self, test_expenses):
        """Test getting expenses via service"""
        service = ExpenseService()
        
        expenses = await service.get_expenses(skip=0, limit=10)
        
        assert len(expenses) == 3
        # Check that telegram_id is attached
        assert all(hasattr(expense, 'telegram_id') for expense in expenses)

    @pytest.mark.asyncio
    async def test_get_expense_by_id_service(self, test_expenses):
        """Test getting expense by ID via service"""
        service = ExpenseService()
        expense_id = test_expenses[0].id
        
        expense = await service.get_expense(expense_id)
        
        assert expense is not None
        assert expense.id == expense_id
        assert hasattr(expense, 'telegram_id')

    @pytest.mark.asyncio
    async def test_get_expense_not_found_service(self):
        """Test getting non-existent expense via service"""
        service = ExpenseService()
        
        expense = await service.get_expense(99999)
        
        assert expense is None

    @pytest.mark.asyncio
    async def test_delete_expense_service(self, test_expenses):
        """Test deleting expense via service"""
        service = ExpenseService()
        expense_id = test_expenses[0].id
        
        success = await service.delete_expense(expense_id)
        
        assert success is True

    @pytest.mark.asyncio
    async def test_delete_expense_not_found_service(self):
        """Test deleting non-existent expense via service"""
        service = ExpenseService()
        
        success = await service.delete_expense(99999)
        
        assert success is False

    @pytest.mark.asyncio
    async def test_update_expense_service(self, test_expenses):
        """Test updating expense via service"""
        service = ExpenseService()
        expense_id = test_expenses[0].id
        
        class ExpenseUpdate:
            description = "Updated Food"
            amount = 30.00
            category = "Food"
        
        expense_update = ExpenseUpdate()
        
        result = await service.update_expense(expense_id, expense_update)
        
        assert result is not None
        assert hasattr(result, 'telegram_id')

    @pytest.mark.asyncio
    async def test_update_expense_not_found_service(self):
        """Test updating non-existent expense via service"""
        service = ExpenseService()
        
        class ExpenseUpdate:
            description = "Updated Food"
            amount = 30.00
            category = "Food"
        
        expense_update = ExpenseUpdate()
        
        result = await service.update_expense(99999, expense_update)
        
        assert result is None
