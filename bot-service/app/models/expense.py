from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import MoneyType
from sqlalchemy_utils.types import Money
from app.models.base import Base


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Money, nullable=False)
    category = Column(Text, nullable=False)
    added_at = Column(TIMESTAMP, nullable=False)