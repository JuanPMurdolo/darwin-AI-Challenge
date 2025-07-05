from groq import Groq
from langchain_core.messages import HumanMessage
from app.core.config import OPENAI_API_KEY
import logging
import json
import os

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

logger = logging.getLogger(__name__)

CATEGORIES = [
    "Housing", "Transportation", "Food", "Utilities", "Insurance",
    "Medical/Healthcare", "Savings", "Debt", "Education", "Entertainment", "Other"
]

async def categorize_expense(text: str):
    logger.info(f"Text to categorize: {text}")
    if text is None or text.strip() == "":
        logger.warning("Empty text provided for categorization.")
        return "Misc", 0.0, "No description"
    #If text doesn't contain any numbers, return Misc category
    if not any(char.isdigit() for char in text):
        logger.warning("No numbers found in text. Categorizing as Misc.")
        return "Misc", 0.0, text
    # Prepare the prompt for LangChain
    #if the text is too long, truncate it to 50 characters
    if len(text) > 50:
        text = text[:50]
        logger.warning("Text truncated to 50 characters for categorization.")

    prompt = f"""
You are an expense analyzer. The user wrote: "{text}".
Extract the category (e.g. Food, Transport) from this categories "{CATEGORIES}", amount (as float), and a short description. Don't use any other words or context that the user might provide. Just expenses.
Respond in JSON format like this: {{"category": "Food", "amount": 10.5, "description": "Pizza"}}
"""
    logger.info(f"LangChain prompt: {prompt}")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=os.environ.get("MODEL_NAME"),
        )
        logger.info(f"LangChain response: {chat_completion}")
        
        logger.info(f"LangChain response: {chat_completion.choices[0].message.content}")

        parsed = json.loads(chat_completion.choices[0].message.content)
        return parsed["category"], float(parsed["amount"]), parsed["description"]
    
    except Exception as e:
        logger.warning(f"LangChain error: {e}. Using mock categorization.")

        # 🧪 Mock categorization fallback
        words = text.lower().split()
        amount = next((float(w) for w in words if w.replace(".", "", 1).isdigit()), 0.0)
        category = "Misc"
        description = text

        return category, amount, description