import { ExpenseBot } from "./src/bot.js"
import { logger } from "./src/utils/logger.js"
import "./src/server.js" // Start the HTTP server

async function main() {
  try {
    const bot = new ExpenseBot()
    await bot.start()

    // Handle graceful shutdown
    process.on("SIGINT", () => {
      logger.info("Received SIGINT, shutting down gracefully")
      bot.stop()
      process.exit(0)
    })

    process.on("SIGTERM", () => {
      logger.info("Received SIGTERM, shutting down gracefully")
      bot.stop()
      process.exit(0)
    })
  } catch (error) {
    logger.error("Failed to start application:", error)
    process.exit(1)
  }
}

main()
