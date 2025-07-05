from pydantic import BaseModel, Field
from typing import Optional

class ExpenseInput(BaseModel):
    user_id: int = Field(..., description="ID interno del usuario (opcional si usás solo telegram_id)")
    description: str = Field(..., description="Descripción de la compra")
    amount: float = Field(..., description="Monto del gasto")
    category: Optional[str] = Field(None, description="Categoría del gasto, si ya viene definida")
    telegram_id: str = Field(..., description="ID del usuario en Telegram")
    text: Optional[str] = Field(None, description="Texto original del mensaje para categorizar")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "description": "Pizza",
                "amount": 20.0,
                "category": "Food",
                "telegram_id": "5440711730",
                "text": "Pizza 20"
            }
        }