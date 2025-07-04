# darwin-AI-Challenge

# Telegram Expense Tracking Bot

A sophisticated Telegram bot system that allows users to track expenses through natural language messages. The system uses AI to parse and categorize expenses automatically.

## Architecture

The system consists of two microservices:

### 1. Bot Service (Python)
- **Technology**: FastAPI, LangChain, OpenAI, PostgreSQL
- **Purpose**: Processes messages using AI to extract and categorize expenses
- **Features**: 
  - Natural language processing with LangChain + OpenAI
  - Automatic expense categorization
  - User whitelist verification
  - Concurrent request handling

### 2. Connector Service (Node.js)
- **Technology**: Node.js, Express, Telegram Bot API
- **Purpose**: Handles Telegram interactions and forwards messages to Bot Service
- **Features**:
  - Telegram webhook/polling management
  - Message routing and response handling
  - Error management and user feedback

## Features

✅ **Natural Language Processing**: Users can send messages like "Pizza 20 bucks" or "Gas $45"  
✅ **Automatic Categorization**: AI categorizes expenses into predefined categories  
✅ **User Whitelist**: Only authorized users can use the bot  
✅ **Concurrent Processing**: Handles multiple users simultaneously  
✅ **Error Handling**: Graceful handling of invalid messages and errors  
✅ **Easy Deployment**: Ready for Vercel, Railway, or other PaaS platforms  

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js LTS (18+)
- PostgreSQL database
- OpenAI API key
- Telegram Bot Token

### 1. Database Setup

\`\`\`bash
# Set up PostgreSQL and run the setup script
psql -d your_database -f scripts/01-create-database.sql
\`\`\`

### 2. Bot Service Setup

\`\`\`bash
cd bot-service
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python main.py
\`\`\`

### 3. Connector Service Setup

\`\`\`bash
cd connector-service
npm install
cp .env.example .env
# Edit .env with your configuration
npm start
\`\`\`

## Configuration

### Environment Variables

**Bot Service (.env)**:
\`\`\`env
DATABASE_URL=postgresql://username:password@localhost:5432/expense_bot
OPENAI_API_KEY=your_openai_api_key
PORT=8000
\`\`\`

**Connector Service (.env)**:
\`\`\`env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
BOT_SERVICE_URL=http://localhost:8000
PORT=3000
\`\`\`

### Adding Users to Whitelist

Add Telegram user IDs to the database:

\`\`\`sql
INSERT INTO users (telegram_id) VALUES ('123456789');
\`\`\`

To find a user's Telegram ID, you can use bots like @userinfobot.

## Usage Examples

Once the bot is running, users can send messages like:

- "Coffee 5 dollars" → Food expense added ✅
- "Uber ride $15" → Transportation expense added ✅
- "Electric bill 120" → Utilities expense added ✅
- "Movie tickets 25 bucks" → Entertainment expense added ✅

## Categories

The bot automatically categorizes expenses into:
- Housing
- Transportation  
- Food
- Utilities
- Insurance
- Medical/Healthcare
- Savings
- Debt
- Education
- Entertainment
- Other

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy!

### Railway

1. Connect GitHub repository
2. Set environment variables
3. Deploy both services

### Supabase (Database)

1. Create a new Supabase project
2. Run the SQL script in the SQL editor
3. Use the connection string in your environment variables

## API Documentation

### Bot Service

**POST /process-message**
\`\`\`json
{
  "telegram_id": "123456789",
  "message": "Pizza 20 bucks"
}
\`\`\`

**Response**:
\`\`\`json
{
  "success": true,
  "message": "Food expense added ✅",
  "category": "Food"
}
\`\`\`

### Health Checks

Both services provide health check endpoints:
- Bot Service: `GET /health`
- Connector Service: `GET /health`

## Development

### Running in Development

**Terminal 1 (Bot Service)**:
\`\`\`bash
cd bot-service
python main.py
\`\`\`

**Terminal 2 (Connector Service)**:
\`\`\`bash
cd connector-service
npm run dev
\`\`\`

### Testing

Test the bot service directly:
\`\`\`bash
curl -X POST http://localhost:8000/process-message \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": "123456789", "message": "Coffee 5 dollars"}'
\`\`\`

## Best Practices Implemented

- ✅ **Microservices Architecture**: Separation of concerns
- ✅ **Environment Configuration**: No hardcoded values
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Logging**: Structured logging throughout
- ✅ **Database Connection Pooling**: Efficient database usage
- ✅ **Type Safety**: Pydantic models and TypeScript support
- ✅ **Graceful Shutdown**: Proper cleanup on termination
- ✅ **Health Checks**: Monitoring and debugging support

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check if both services are running and can communicate
2. **Database connection errors**: Verify DATABASE_URL and database accessibility
3. **OpenAI API errors**: Check API key and rate limits
4. **Telegram webhook issues**: Ensure bot token is correct and bot is started
