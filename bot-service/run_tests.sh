#!/bin/bash

echo "🧪 Running Darwin AI Challenge Tests"
echo "=================================="

# Set testing flag
export TESTING=1

# Check if we're running inside Docker or locally
if [ -f /.dockerenv ]; then
    echo "🐳 Running inside Docker container"
    export TESTING_IN_DOCKER=1
    export DATABASE_URL="postgresql+asyncpg://expenses_user:expenses_pass@postgres:5432/expenses_db"
else
    echo "💻 Running locally"
    
    # Try to install psycopg2-binary if not available
    echo "📦 Checking PostgreSQL dependencies..."
    python -c "import psycopg2" 2>/dev/null || {
        echo "⚠️  psycopg2 not found, installing..."
        pip install psycopg2-binary 2>/dev/null || {
            echo "❌ Could not install psycopg2-binary, will use SQLite for testing"
            export DATABASE_URL="sqlite+aiosqlite:///./test.db"
        }
    }
    
    # Check if Docker services are running and psycopg2 is available
    if docker compose ps | grep -q "Up" && python -c "import psycopg2" 2>/dev/null; then
        echo "✅ Docker services detected with PostgreSQL support"
        export DATABASE_URL="postgresql+asyncpg://expenses_user:expenses_pass@localhost:5433/expenses_db"
    else
        echo "ℹ️  Using SQLite for local testing"
        export DATABASE_URL="sqlite+aiosqlite:///./test.db"
    fi
fi

# Install dependencies if not already installed
echo "📦 Installing test dependencies..."
pip install pytest pytest-asyncio httpx aiosqlite > /dev/null 2>&1

# Test database connectivity based on the URL
echo ""
echo "🔌 Testing database connectivity..."
if [[ $DATABASE_URL == *"sqlite"* ]]; then
    echo "✅ Using SQLite for testing (no connectivity test needed)"
    DB_AVAILABLE=0
else
    python -c "
import asyncio
import sys

async def test_db():
    try:
        import asyncpg
        conn = await asyncpg.connect('$DATABASE_URL', timeout=5)
        await conn.close()
        print('✅ PostgreSQL connection successful')
        return True
    except ImportError:
        print('❌ asyncpg not available')
        return False
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        return False

result = asyncio.run(test_db())
sys.exit(0 if result else 1)
"
    DB_AVAILABLE=$?
fi

if [ $DB_AVAILABLE -eq 0 ]; then
    echo ""
    echo "✅ Database available - running full test suite..."
    pytest tests/ -v
else
    echo ""
    echo "⚠️  Database not available - running tests without database dependency"
    echo "   Note: Some integration tests will be skipped"
    pytest tests/test_schemas.py tests/test_analytics_simple.py tests/test_health_simple.py tests/test_environment.py -v
fi

echo ""
echo "✅ Test run complete!"
echo ""
echo "💡 Recommendations:"
echo "   - For full testing: make test-docker (runs tests in Docker)"
echo "   - For service testing: make test-services (tests HTTP APIs)"
echo "   - For local PostgreSQL: pip install psycopg2-binary"
