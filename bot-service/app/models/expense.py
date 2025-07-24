from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from app.models.base import Base


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    category = Column(Text, nullable=False)
    added_at = Column(TIMESTAMP, nullable=False)