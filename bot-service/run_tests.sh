#!/bin/bash

echo "🧪 Running Darwin AI Challenge Tests - Fixed Version"
echo "=================================================="

export TESTING=1

export DATABASE_URL="sqlite+aiosqlite:///./test.db"
echo "ℹ️  Using SQLite for local testing"

echo "📦 Installing test dependencies..."
pip install pytest pytest-asyncio httpx aiosqlite > /dev/null 2>&1

rm -f ./test.db

echo ""
echo "✅ Using SQLite for testing (no connectivity test needed)"

echo ""
echo "🔧 Testing Individual Components..."
echo "=================================="

echo "📋 Testing Models (should all pass)..."
pytest tests/test_models.py -v --tb=short

echo ""
echo "💰 Testing Fixed Expense Repository..."
pytest tests/test_expense.py::TestExpenseRepository::test_add_expense_success -v --tb=short

echo ""
echo "📊 Testing Analytics (with DB session fix)..."
pytest tests/test_analytics.py::TestAnalyticsService::test_get_expense_analytics_nonexistent_user -v --tb=short

echo ""
echo "🤖 Testing LangChain Handler..."
pytest tests/test_langchain_handler.py -v --tb=short

echo ""
echo "⚙️  Testing Fixed Celery Tasks..."
pytest tests/test_celery_tasks.py::TestCeleryTasks::test_run_analytics_task_direct_call -v --tb=short

echo ""
echo "🌐 Testing Integration (AsyncClient working)..."
echo "=============================================="
pytest tests/integration_test.py::TestHealthEndpoints::test_root_endpoint -v --tb=short
pytest tests/integration_test.py::TestExpenseEndpoints::test_create_expense_success -v --tb=short

echo ""
echo "🔍 Running All Tests (Final Check)..."
echo "===================================="
pytest tests/ -v --tb=short --disable-warnings | head -50

echo ""
echo "✅ Test run complete!"
echo ""

