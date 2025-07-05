from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.core.config import OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

CATEGORIES = [
    "Housing", "Transportation", "Food", "Utilities", "Insurance",
    "Medical/Healthcare", "Savings", "Debt", "Education", "Entertainment", "Other"
]

async def categorize_expense(text: str):
    prompt = f"""Categorize this expense: {text}. Return only: category, amount, description."""
    
    try:
        response = await llm.ainvoke(prompt)
        parsed = response.content.strip().split(",")
        print("Categorized:", parsed)
        if len(parsed) != 3:
            return None
        return [s.strip() for s in parsed]
    except Exception as e:
        print(f"LangChain error: {e}")
        return None
