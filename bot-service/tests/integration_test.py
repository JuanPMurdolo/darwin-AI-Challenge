import asyncio
import httpx

async def test_valid_expense():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/process-message", json={
            "telegram_id": "123456789",
            "message": "Netflix 12.99"
        })
        assert response.status_code == 200
        assert "expense added" in response.json()["message"]

asyncio.run(test_valid_expense())
