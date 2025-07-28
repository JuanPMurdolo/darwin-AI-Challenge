import dotenv from "dotenv"

dotenv.config()

export const config = {
  telegram: {
    botToken: process.env.TELEGRAM_BOT_TOKEN,
  },
  botService: {
    url: process.env.BOT_SERVICE_URL || "http://localhost:8001",
  },
  server: {
    port: process.env.PORT || 3000
  },
  environment: process.env.NODE_ENV || "development",
}

const requiredEnvVars = ["TELEGRAM_BOT_TOKEN"]

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    console.error(`Missing required environment variable: ${envVar}`)
    process.exit(1)
  }
}