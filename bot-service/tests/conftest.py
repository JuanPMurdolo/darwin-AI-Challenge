import pytest
import pytest_asyncio
import asyncio
import os
from httpx import AsyncClient
from app.main import app
from app.core.db import AsyncSessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.models.expense import Expense
from datetime import datetime, date
from decimal import Decimal
from unittest.mock import AsyncMock, patch

# Set testing environment
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a clean database session for each test"""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        yield session
    
    # Clean up after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client():
    """Create an async HTTP client for testing"""
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture
async def test_user(db_session):
    """Create a test user"""
    user = User(id="test_user_123", telegram_id="123456789")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def test_user_2(db_session):
    """Create a second test user"""
    user = User(id="test_user_456", telegram_id="987654321")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def test_expenses(db_session, test_user):
    """Create test expenses"""
    expenses = [
        Expense(
            id=1,
            user_id=test_user.id,
            description="Test Food Expense",
            amount=Decimal("25.50"),
            category="Food",
            added_at=datetime(2024, 1, 15)
        ),
        Expense(
            id=2,
            user_id=test_user.id,
            description="Test Transport Expense",
            amount=Decimal("15.00"),
            category="Transportation",
            added_at=datetime(2024, 1, 20)
        ),
        Expense(
            id=3,
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
    
    # Refresh all expenses
    for expense in expenses:
        await db_session.refresh(expense)
    
    return expenses

@pytest.fixture
def mock_langchain_handler():
    """Mock the langchain handler for consistent testing"""
    with patch('app.handlers.langchain_handler.categorize_expense') as mock:
        # Return more predictable data for testing
        mock.return_value = ("Food", 25.50, "Pizza")
        yield mock

@pytest.fixture
def mock_celery_task():
    """Mock Celery tasks for testing"""
    with patch('app.tasks.analytics.run_analytics_task') as mock:
        mock_result = AsyncMock()
        mock_result.id = "test-task-id"
        mock.delay.return_value = mock_result
        yield mock
