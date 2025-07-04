# Bot Service

Python service that parses and categorizes expenses from Telegram messages using LangChain and OpenAI.

## Features

- Message classification
- Expense categorization
- User whitelist
- Async & concurrent request handling
- PostgreSQL integration

## Setup

1. Install Python 3.11+
2. Create a `.env` file:
    * OPENAI_API_KEY=your_key
    *   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/expenses_db

3. Install deps
```
pip install -r requirements.txt
```

3. Run server:
uvicorn app.main:app --reload --port 8000
or
docker-compose up --build

4. Endpoints:
    * POST /expense/add: Parses a Telegram message and stores the expense
    * GET /expense/list 
    * GET /expense/id
    * DELETE /expense/id
    * PUT /expense/id

5. Testing
python tests/test_integration.py





