from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base

class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)  # ✅ ESTA
    telegram_id = Column(String, unique=True, nullable=True)
    email = Column(String)
    full_name = Column(String)