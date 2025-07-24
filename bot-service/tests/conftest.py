import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.core.db import AsyncSessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.models.expense import Expense
from datetime import datetime, date
from decimal import Decimal

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_client():
    """Create an async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def db_session():
    """Create a database session for testing"""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        yield session
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def test_user(db_session):
    """Create a test user"""
    user = User(id="test_user_123", telegram_id="123456789")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def test_expenses(db_session, test_user):
    """Create test expenses"""
    expenses = [
        Expense(
            user_id=test_user.id,
            description="Test Food Expense",
            amount=Decimal("25.50"),
            category="Food",
            added_at=datetime(2024, 1, 15)
        ),
        Expense(
            user_id=test_user.id,
            description="Test Transport Expense",
            amount=Decimal("15.00"),
            category="Transportation",
            added_at=datetime(2024, 1, 20)
        ),
        Expense(
            user_id=test_user.id,
            description="Test Food Expense 2",
            amount=Decimal("30.00"),
            category="Food",
            added_at=datetime(2024, 2, 10)
        )
    ]
    
    for expense in expenses:
        db_session.add(expense)
    
    await db_session.commit()
    return expenses
