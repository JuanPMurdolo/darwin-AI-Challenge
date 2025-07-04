from app.repositories.expense import ExpenseRepository

class ExpenseService:
    def __init__(self):
        self.expense_repo = ExpenseRepository()

    async def add_expense(self, user_id: int, description: str, amount: float, category: str, telegram_id: str, text: str):
        return await self.expense_repo.add_expense(user_id, description, amount, category, telegram_id, text)

    async def get_expenses(self, user_id: int):
        return await self.expense_repo.get_expenses(user_id)
    
    async def get_expense_by_id(self, expense_id: int):
        return await self.expense_repo.get_expense_by_id(expense_id)
    
    async def delete_expense(self, expense_id: int):
        return await self.expense_repo.delete_expense(expense_id)
    
    async def update_expense(self, expense_id: int, description: str, amount: float, category: str):
        return await self.expense_repo.update_expense(expense_id, description, amount, category)