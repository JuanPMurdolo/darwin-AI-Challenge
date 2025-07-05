import TelegramBot from "node-telegram-bot-api";
import fetch from "node-fetch";
import { config } from "./config.js";
import { logger } from "./utils/logger.js";

class ExpenseBot {
  constructor() {
    this.bot = new TelegramBot(config.telegram.botToken, { polling: true });
    this.setupHandlers();
    logger.info("Telegram bot initialized");
  }

  setupHandlers() {
    this.bot.on("message", async (msg) => {
      await this.handleMessage(msg);
    });

    this.bot.on("error", (error) => {
      logger.error("Telegram bot error:", error.message);
    });

    this.bot.on("polling_error", (error) => {
      logger.error("Telegram polling error:", error.message);
    });

    logger.info("Bot handlers set up successfully");
  }

  async handleMessage(msg) {
    const chatId = msg.chat.id;
    const telegramId = msg.from.id.toString();
    const messageText = msg.text;

    if (!messageText) return;

    logger.info(`Message from ${telegramId}: ${messageText}`);

    try {
      const response = await this.sendToBotService(telegramId, messageText);
      logger.info(`Response from bot service: ${JSON.stringify(response)}`);

      if (response.status.success) {
        await this.bot.sendMessage(chatId, response.message);
        logger.info(`Expense processed for user ${telegramId}`);
      } else {
        await this.bot.sendMessage(chatId, "Expense could not be processed.");
        logger.warn(`Unsuccessful processing for user ${telegramId}`);
      }
    } catch (error) {
      await this.handleError(chatId, error);
    }
  }

  async sendToBotService(telegramId, messageText) {
    const url = `${config.botService.url}/expense/add`;

    const payload = {
      telegram_id: telegramId,
      text: messageText,
      description: null,
      amount: null,
      category: null,
      user_id: null
    };

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const detail = errorData.detail || "Unknown error";

      if (response.status === 403) throw new Error("USER_NOT_AUTHORIZED");
      if (response.status === 400) throw new Error("NOT_AN_EXPENSE");
      throw new Error(`BOT_SERVICE_ERROR: ${detail}`);
    }

    return await response.json();
  }

  async handleError(chatId, error) {
    const message = error.message || error.toString();

    logger.error(`Error processing message: ${message}`);

    switch (message) {
      case "USER_NOT_AUTHORIZED":
        logger.info(`Unauthorized user tried to use bot: ${chatId}`);
        break;

      case "NOT_AN_EXPENSE":
        logger.info(`Non-expense message ignored from user: ${chatId}`);
        break;

      default:
        await this.bot.sendMessage(
          chatId,
          "Sorry, I encountered an error processing your message. Please try again."
        );
        break;
    }
  }

  async start() {
    try {
      const me = await this.bot.getMe();
      logger.info(`Bot started successfully: @${me.username}`);
      await this.testBotServiceConnection();
    } catch (error) {
      logger.error("Failed to start bot:", error.message);
      process.exit(1);
    }
  }

  async testBotServiceConnection() {
    try {
      const response = await fetch(`${config.botService.url}/health`);
      if (response.ok) {
        logger.info("Bot service connection successful");
      } else {
        throw new Error(`Bot service health check failed: ${response.status}`);
      }
    } catch (error) {
      logger.error("Bot service connection failed:", error.message);
      throw error;
    }
  }

  stop() {
    this.bot.stopPolling();
    logger.info("Bot stopped");
  }
}

export { ExpenseBot };
