import pytest
from app.models.user import User
from app.models.expense import Expense
from datetime import datetime
from decimal import Decimal

class TestUserModel:
    """Unit tests for User model"""
    
    def test_user_creation(self):
        """Test creating a user instance"""
        user = User(id="test_user", telegram_id="123456789")
        
        assert user.id == "test_user"
        assert user.telegram_id == "123456789"

    def test_user_with_none_telegram_id(self):
        """Test creating user with None telegram_id"""
        user = User(id="test_user", telegram_id=None)
        
        assert user.id == "test_user"
        assert user.telegram_id is None

    @pytest.mark.asyncio
    async def test_user_database_operations(self, db_session):
        """Test user database operations"""
        # Create user
        user = User(id="db_test_user", telegram_id="987654321")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Verify user was saved
        assert user.id == "db_test_user"
        assert user.telegram_id == "987654321"


class TestExpenseModel:
    """Unit tests for Expense model"""
    
    def test_expense_creation(self):
        """Test creating an expense instance"""
        expense = Expense(
            user_id="test_user",
            description="Test expense",
            amount=Decimal("25.50"),
            category="Food",
            added_at=datetime(2024, 1, 15)
        )
        
        assert expense.user_id == "test_user"
        assert expense.description == "Test expense"
        assert expense.amount == Decimal("25.50")
        assert expense.category == "Food"
        assert expense.added_at == datetime(2024, 1, 15)

    def test_expense_with_large_amount(self):
        """Test expense with large amount"""
        expense = Expense(
            user_id="test_user",
            description="Expensive item",
            amount=Decimal("9999.99"),
            category="Other",
            added_at=datetime.now()
        )
        
        assert expense.amount == Decimal("9999.99")

    def test_expense_with_zero_amount(self):
        """Test expense with zero amount"""
        expense = Expense(
            user_id="test_user",
            description="Free item",
            amount=Decimal("0.00"),
            category="Other",
            added_at=datetime.now()
        )
        
        assert expense.amount == Decimal("0.00")

    @pytest.mark.asyncio
    async def test_expense_database_operations(self, db_session, test_user):
        """Test expense database operations"""
        # Create expense
        expense = Expense(
            user_id=test_user.id,
            description="Database test expense",
            amount=Decimal("15.75"),
            category="Transportation",
            added_at=datetime(2024, 1, 20)
        )
        
        db_session.add(expense)
        await db_session.commit()
        await db_session.refresh(expense)
        
        # Verify expense was saved
        assert expense.id is not None
        assert expense.user_id == test_user.id
        assert expense.description == "Database test expense"
        assert expense.amount == Decimal("15.75")
        assert expense.category == "Transportation"

    @pytest.mark.asyncio
    async def test_expense_foreign_key_relationship(self, db_session):
        """Test expense foreign key relationship with user"""
        # Create user first
        user = User(id="fk_test_user", telegram_id="111222333")
        db_session.add(user)
        await db_session.commit()
        
        # Create expense with valid user_id
        expense = Expense(
            user_id=user.id,
            description="FK test expense",
            amount=Decimal("10.00"),
            category="Food",
            added_at=datetime.now()
        )
        
        db_session.add(expense)
        await db_session.commit()
        await db_session.refresh(expense)
        
        assert expense.user_id == user.id

    def test_expense_decimal_precision(self):
        """Test expense amount decimal precision"""
        expense = Expense(
            user_id="test_user",
            description="Precision test",
            amount=Decimal("123.456"),  # More than 2 decimal places
            category="Other",
            added_at=datetime.now()
        )
        
        # The model should handle the precision as defined in the column
        assert expense.amount == Decimal("123.456")
