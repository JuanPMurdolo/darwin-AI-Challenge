import express from "express"
import { config } from "./config.js"
import { logger } from "./utils/logger.js"
import './bot.js'

const app = express()

// Middleware
app.use(express.json())

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "connector-service",
    timestamp: new Date().toISOString(),
  })
})


const bot = new ExpenseBot();
bot.start();


// Start server
const server = app.listen(config.server.port, () => {
  logger.info(`Connector service listening on port ${config.server.port}`)
})

// Graceful shutdown
process.on("SIGTERM", () => {
  logger.info("SIGTERM received, shutting down gracefully")
  server.close(() => {
    logger.info("Server closed")
    process.exit(0)
  })
})

export { app }
