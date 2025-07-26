from app.repositories.expense import ExpenseRepository

class ExpenseService:
    def __init__(self):
        self.expense_repo = ExpenseRepository()


    async def create_expense(self, expense_data: dict):
        user_id = expense_data.user_id
        description = expense_data.description
        amount = expense_data.amount
        category = expense_data.category
        telegram_id = expense_data.telegram_id
        text = expense_data.text
        if not all([user_id, description, amount, category, telegram_id, text]):
            raise ValueError("All fields are required to create an expense.")
        return await self.expense_repo.add_expense(
            user_id=user_id,
            description=description,
            amount=amount,
            category=category,
            telegram_id=telegram_id,
            text=text
        )

    async def get_expenses(self, skip: int = 0, limit: int = 10):
        return await self.expense_repo.get_all_expenses(skip=skip, limit=limit)
        
    
    async def get_expense_by_id(self, expense_id: int):
        return await self.expense_repo.get_expense_by_id(expense_id)
    
    async def delete_expense(self, expense_id: int):
        return await self.expense_repo.delete_expense(expense_id)
    
    async def update_expense(self, expense_id: int, description: str, amount: float, category: str):
        return await self.expense_repo.update_expense(expense_id, description, amount, category)
    
    async def get_expense_analytics(self, user_id: int, start_date: str, end_date: str):
        return await self.expense_repo.get_expense_analytics(user_id, start_date, end_date)
