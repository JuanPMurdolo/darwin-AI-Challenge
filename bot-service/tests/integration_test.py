import pytest
from httpx import AsyncClient
import json
from datetime import date
from unittest.mock import patch, AsyncMock

class TestExpenseEndpoints:
    """Integration tests for expense endpoints"""

    @pytest.mark.asyncio
    async def test_create_expense_success(self, async_client: AsyncClient, test_user, mock_langchain_handler):
        """Test creating expense via API"""
        payload = {
            "user_id": "1",
            "description": "Pizza",
            "amount": 25.50,
            "category": "Food",
            "telegram_id": test_user.telegram_id,
            "text": "Pizza 25.50"
        }
        
        response = await async_client.post("/api/expenses/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 25.50

    @pytest.mark.asyncio
    async def test_create_expense_invalid_data(self, async_client: AsyncClient):
        """Test creating expense with invalid data"""
        payload = {
            "user_id": "",
            "description": "Pizza",
            "amount": 25.50,
            "category": "Food",
            "telegram_id": "123456789",
            "text": "Pizza 25.50"
        }
        
        response = await async_client.post("/api/expenses/", json=payload)
        assert response.status_code == 500

    @pytest.mark.asyncio
    async def test_get_expenses(self, async_client: AsyncClient, test_expenses):
        """Test getting all expenses"""
        response = await async_client.get("/api/expenses/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 3
        assert all("telegram_id" in expense for expense in data)

    @pytest.mark.asyncio
    async def test_get_expenses_with_pagination(self, async_client: AsyncClient, test_expenses):
        """Test getting expenses with pagination"""
        response = await async_client.get("/api/expenses/?skip=1&limit=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_delete_expense(self, async_client: AsyncClient, test_expenses):
        """Test deleting expense"""
        expense_id = test_expenses[0].id
        response = await async_client.delete(f"/api/expenses/{expense_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Expense deleted successfully"

class TestAnalyticsEndpoints:
    """Integration tests for analytics endpoints"""

    @pytest.mark.asyncio
    async def test_analytics_sync_endpoint(self, async_client: AsyncClient, test_user, test_expenses):
        """Test synchronous analytics endpoint"""
        response = await async_client.get(
            f"/api/analytics/sync?user_id={test_user.id}&start_date=2024-01-01&end_date=2024-01-31"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_expenses"] == 40.50
        assert len(data["category_breakdown"]) == 2
        assert "Food" in data["average_by_category"]
        assert "Transportation" in data["average_by_category"]

    @pytest.mark.asyncio
    async def test_analytics_sync_no_dates(self, async_client: AsyncClient, test_user, test_expenses):
        """Test sync analytics without date parameters"""
        response = await async_client.get(f"/api/analytics/sync?user_id={test_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_expenses"] == 70.50

    @pytest.mark.asyncio
    async def test_task_status_pending(self, async_client: AsyncClient):
        """Test task status for pending task"""
        with patch('app.routes.analytics.AsyncResult') as mock_result:
            mock_task = AsyncMock()
            mock_task.state = "PENDING"
            mock_result.return_value = mock_task
            
            response = await async_client.get("/api/analytics/status/test-task-id")
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "PENDING"

    @pytest.mark.asyncio
    async def test_task_status_failure(self, async_client: AsyncClient):
        """Test task status for failed task"""
        with patch('app.routes.analytics.AsyncResult') as mock_result:
            mock_task = AsyncMock()
            mock_task.state = "FAILURE"
            mock_task.result = Exception("Task failed")
            mock_result.return_value = mock_task
            
            response = await async_client.get("/api/analytics/status/test-task-id")
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "FAILED"
            assert "error" in data

    @pytest.mark.asyncio
    async def test_overview_endpoint(self, async_client: AsyncClient, test_user, test_expenses):
        """Test overview endpoint"""
        response = await async_client.get(f"/api/analytics/overview/{test_user.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_expenses" in data
        assert "expense_count" in data
        assert "average_expense" in data
        assert "monthly_variation_percentage" in data

    @pytest.mark.asyncio
    async def test_category_summary_endpoint(self, async_client: AsyncClient, test_user, test_expenses):
        """Test category summary endpoint"""
        response = await async_client.get(f"/api/analytics/category-summary/{test_user.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert all("category" in item and "total" in item for item in data)


class TestHealthEndpoints:
    """Integration tests for health endpoints"""

    @pytest.mark.asyncio
    async def test_readiness_endpoint(self, async_client: AsyncClient):
        """Test readiness check endpoint"""
        response = await async_client.get("/health/ready")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    @pytest.mark.asyncio
    async def test_liveness_endpoint(self, async_client: AsyncClient):
        """Test liveness check endpoint"""
        response = await async_client.get("/health/live")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "alive"

    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_client: AsyncClient):
        """Test root endpoint"""
        response = await async_client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Darwin AI Expense Tracker API"
        assert data["status"] == "running"

    @pytest.mark.asyncio
    async def test_health_check_endpoint(self, async_client: AsyncClient):
        """Test main health check endpoint"""
        response = await async_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "database" in data


class TestErrorHandling:
    """Integration tests for error handling"""

    @pytest.mark.asyncio
    async def test_404_endpoint(self, async_client: AsyncClient):
        """Test non-existent endpoint"""
        response = await async_client.get("/nonexistent")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_invalid_json(self, async_client: AsyncClient):
        """Test invalid JSON payload"""
        response = await async_client.post(
            "/api/expenses/", 
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_missing_required_fields(self, async_client: AsyncClient):
        """Test missing required fields in request"""
        payload = {
            "description": "Pizza"
        }
        
        response = await async_client.post("/api/expenses/", json=payload)
        assert response.status_code == 422
