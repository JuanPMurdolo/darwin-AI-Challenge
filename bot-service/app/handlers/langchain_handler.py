from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.schema import HumanMessage
from app.core.config import OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

CATEGORIES = [
    "Housing", "Transportation", "Food", "Utilities", "Insurance",
    "Medical/Healthcare", "Savings", "Debt", "Education", "Entertainment", "Other"
]

async def categorize_expense(message: str) -> tuple[str, float, str] | None:
    prompt = (
        f"Categorize expnse: {', '.join(CATEGORIES)}. "
        "Also, extract the amount and the description.\n"
        f"Input Example: 'Pizza 20 bucks'\n"
        "Response: Food, 20, Pizza\n\n"
        f"Input: {message}"
    )
    response = await llm.ainvoke(prompt)
    result = response
    
    try:
        category, amount, description = [x.strip() for x in response.split(",")]
        return category, float(amount), description
    except:
        return None
