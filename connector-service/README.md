# Connector Service

Node.js service that handles Telegram bot interactions and forwards messages to the Bot Service for processing.

## Features

- Telegram Bot API integration
- Message forwarding to Bot Service
- User whitelist enforcement (handled by Bot Service)
- Graceful error handling
- Health check endpoint

## Setup

### Prerequisites

- Node.js LTS (18+)
- Telegram Bot Token (from @BotFather)
- Running Bot Service

### Installation

1. Install dependencies:
\`\`\`bash
npm install
\`\`\`

2. Set up environment variables:
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### Configuration

Required environment variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `BOT_SERVICE_URL`: URL of the Bot Service (default: http://localhost:8000)
- `PORT`: Service port (default: 3000)

### Getting a Telegram Bot Token

1. Message @BotFather on Telegram
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the token to your `.env` file

### Running

Development:
\`\`\`bash
npm run dev
\`\`\`

Production:
\`\`\`bash
npm start
\`\`\`

## Architecture

The connector service:
1. Receives messages from Telegram users
2. Forwards messages to the Bot Service via HTTP
3. Handles responses and sends them back to users
4. Manages errors gracefully (ignores unauthorized users and non-expenses)

## API Endpoints

### GET /health
Health check endpoint.

Response:
\`\`\`json
{
  "status": "healthy",
  "service": "connector-service",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
\`\`\`

## Deployment

The service can be deployed to:
- Vercel
- Railway
- Heroku
- Any Node.js hosting platform

Make sure to set the environment variables in your deployment platform.
