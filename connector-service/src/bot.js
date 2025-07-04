import TelegramBot from "node-telegram-bot-api"
import fetch from "node-fetch"
import { config } from "./config.js"
import { logger } from "./utils/logger.js"

class ExpenseBot {
  constructor() {
    this.bot = new TelegramBot(config.telegram.botToken, { polling: true })
    this.setupHandlers()
    logger.info("Telegram bot initialized")
  }

  setupHandlers() {
    // Handle all text messages
    this.bot.on("message", async (msg) => {
      await this.handleMessage(msg)
    })

    // Handle errors
    this.bot.on("error", (error) => {
      logger.error("Telegram bot error:", error)
    })

    // Handle polling errors
    this.bot.on("polling_error", (error) => {
      logger.error("Telegram polling error:", error)
    })

    logger.info("Bot handlers set up successfully")
  }

  async handleMessage(msg) {
    const chatId = msg.chat.id
    const telegramId = msg.from.id.toString()
    const messageText = msg.text

    // Log incoming message
    logger.info(`Message from ${telegramId}: ${messageText}`)

    // Skip non-text messages
    if (!messageText) {
      return
    }

    try {
      // Send message to bot service for processing
      const response = await this.processWithBotService(telegramId, messageText)

      if (response.success) {
        // Send success response
        await this.bot.sendMessage(chatId, response.message)
        logger.info(`Expense processed successfully for user ${telegramId}`)
      }
    } catch (error) {
      await this.handleError(chatId, error)
    }
  }

  async processWithBotService(telegramId, message) {
    const url = `${config.botService.url}/expense/add`

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        telegram_id: telegramId,
        message: message,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))

      if (response.status === 403) {
        throw new Error("USER_NOT_AUTHORIZED")
      } else if (response.status === 400) {
        throw new Error("NOT_AN_EXPENSE")
      } else {
        throw new Error(`Bot service error: ${errorData.detail || "Unknown error"}`)
      }
    }

    return await response.json()
  }

  async handleError(chatId, error) {
    logger.error("Error processing message:", error.message)

    switch (error.message) {
      case "USER_NOT_AUTHORIZED":
        // Silently ignore unauthorized users (as per requirements)
        logger.info(`Unauthorized user attempted to use bot: ${chatId}`)
        break

      case "NOT_AN_EXPENSE":
        // Silently ignore non-expense messages (as per requirements)
        logger.info(`Non-expense message ignored from user: ${chatId}`)
        break

      default:
        // Send generic error message for other errors
        await this.bot.sendMessage(chatId, "Sorry, I encountered an error processing your message. Please try again.")
        break
    }
  }

  async start() {
    try {
      const me = await this.bot.getMe()
      logger.info(`Bot started successfully: @${me.username}`)

      // Test bot service connection
      await this.testBotServiceConnection()
    } catch (error) {
      logger.error("Failed to start bot:", error)
      process.exit(1)
    }
  }

  async testBotServiceConnection() {
    try {
      const response = await fetch(`${config.botService.url}/health`)
      if (response.ok) {
        logger.info("Bot service connection successful")
      } else {
        throw new Error(`Bot service health check failed: ${response.status}`)
      }
    } catch (error) {
      logger.error("Bot service connection failed:", error.message)
      throw error
    }
  }

  stop() {
    this.bot.stopPolling()
    logger.info("Bot stopped")
  }
}

export { ExpenseBot }
