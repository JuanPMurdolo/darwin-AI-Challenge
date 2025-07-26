from app.repositories.expense import ExpenseRepository

class ExpenseService:
    def __init__(self):
        self.expense_repo = ExpenseRepository()

    async def create_expense(self, user_id: int, description: str, amount: float, category: str):
        return await self.expense_repo.create_expense(user_id, description, amount, category)
        
    async def get_expenses(self, user_id: int):
        return await self.expense_repo.get_expenses(user_id)
    
    async def get_expense_by_id(self, expense_id: int):
        return await self.expense_repo.get_expense_by_id(expense_id)
    
    async def delete_expense(self, expense_id: int):
        return await self.expense_repo.delete_expense(expense_id)
    
    async def update_expense(self, expense_id: int, description: str, amount: float, category: str):
        return await self.expense_repo.update_expense(expense_id, description, amount, category)
    
    async def get_expense_analytics(self, user_id: int, start_date: str, end_date: str):
        return await self.expense_repo.get_expense_analytics(user_id, start_date, end_date)
