import pytest
from httpx import AsyncClient
import json
from datetime import date

class TestAnalyticsIntegration:
    """Integration tests for analytics endpoint"""
    
    @pytest.mark.asyncio
    async def test_analytics_endpoint_async(self, async_client: AsyncClient, test_user, test_expenses):
        """Test async analytics endpoint"""
        payload = {
            "user_id": test_user.id,
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        }
        
        # Create analytics task
        response = await async_client.post("/analytics/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "PENDING"
        
        task_id = data["task_id"]
        
        # Check task status (might need to wait for completion in real scenario)
        status_response = await async_client.get(f"/analytics/status/{task_id}")
        assert status_response.status_code == 200
        
        status_data = status_response.json()
        assert status_data["task_id"] == task_id
        assert status_data["status"] in ["PENDING", "SUCCESS", "FAILURE"]

    @pytest.mark.asyncio
    async def test_analytics_sync_endpoint(self, async_client: AsyncClient, test_user, test_expenses):
        """Test synchronous analytics endpoint"""
        response = await async_client.get(
            f"/analytics/sync?user_id={test_user.id}&start_date=2024-01-01&end_date=2024-01-31"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_expenses"] == 40.50
        assert len(data["category_breakdown"]) == 2
        assert "Food" in data["average_by_category"]
        assert "Transportation" in data["average_by_category"]

    @pytest.mark.asyncio
    async def test_health_endpoint(self, async_client: AsyncClient):
        """Test health check endpoint"""
        response = await async_client.get("/health/")
        
        # Might return 503 if services are not available, but should not crash
        assert response.status_code in [200, 503]
        
        data = response.json()
        assert "status" in data
        assert "checks" in data
        assert "database" in data["checks"]

    @pytest.mark.asyncio
    async def test_invalid_analytics_request(self, async_client: AsyncClient):
        """Test analytics endpoint with invalid data"""
        payload = {
            "user_id": "",  # Invalid empty user_id
            "start_date": "invalid-date",
            "end_date": "2024-01-31"
        }
        
        response = await async_client.post("/analytics/", json=payload)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_task_status_nonexistent(self, async_client: AsyncClient):
        """Test task status for non-existent task"""
        response = await async_client.get("/analytics/status/nonexistent-task-id")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] in ["PENDING", "FAILURE"]  # Celery returns PENDING for unknown tasks
