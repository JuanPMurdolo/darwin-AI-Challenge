from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from app.models.base import Base

class User(Base):
    
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=True)