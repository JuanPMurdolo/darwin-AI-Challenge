import express from "express"
import { config } from "./config.js"
import { logger } from "./utils/logger.js"
import { ExpenseBot } from "./bot.js";

const app = express()

app.use(express.json())

app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "connector-service",
    timestamp: new Date().toISOString(),
  })
})

const server = app.listen(config.server.port, () => {
  logger.info(`Connector service listening on port ${config.server.port}`)
})

const bot = new ExpenseBot();
bot.start();

process.on("SIGTERM", () => {
  logger.info("SIGTERM received, shutting down gracefully")
  server.close(() => {
    logger.info("Server closed")
    process.exit(0)
  })
})

export { app }
