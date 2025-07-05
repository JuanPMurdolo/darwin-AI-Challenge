from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.core.config import OPENAI_API_KEY
import logging

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)

CATEGORIES = [
    "Housing", "Transportation", "Food", "Utilities", "Insurance",
    "Medical/Healthcare", "Savings", "Debt", "Education", "Entertainment", "Other"
]

async def categorize_expense(text: str):
    logger.info(f"Text to categorize: {text}")

    prompt = f"""
You are an expense analyzer. The user wrote: "{text}".
Extract the category (e.g. Food, Transport), amount (as float), and a short description.
Respond in JSON format like this: {{"category": "Food", "amount": 10.5, "description": "Pizza"}}
"""
    try:
        response = await llm.ainvoke(prompt)
        logger.info(f"LangChain response: {response.content}")

        parsed = json.loads(response.content)
        return parsed["category"], float(parsed["amount"]), parsed["description"]

    except Exception as e:
        logger.warning(f"LangChain error: {e}. Using mock categorization.")

        # 🧪 Mock categorization fallback
        words = text.lower().split()
        amount = next((float(w) for w in words if w.replace(".", "", 1).isdigit()), 0.0)
        category = "Food" if "pizza" in words or "burger" in words else "Misc"
        description = text

        return category, amount, description