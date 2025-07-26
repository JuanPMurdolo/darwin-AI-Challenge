import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.user import User
from app.models.expense import Expense
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy import select

# Load environment variables
load_dotenv()

# Validate DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set in the environment.")

# Config  SQLAlchemy Async
engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_tables():
    """Create database tables if they do not exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully.")
    
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Check if the default user already exists
            result = await session.execute(select(User).where(User.id == "1"))
            user = result.scalars().first()
            if user:
                print("ℹ️ Default user already exists. Skipping creation.")
                return
            user = User(id="1", telegram_id="123456789")
            session.add(user)

            result = await session.execute(select(User).where(User.id == "2"))
            user = result.scalars().first()
            if user:
                print("ℹ️ Default user already exists. Skipping creation.")
                return
            user = User(id="2", telegram_id="5440711730")
            session.add(user)
        await session.commit()
        print("✅ Default user created with ID 1 and telegram_id '123456789'.")

async def get_db():
    """Dependency to get the database session."""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def async_session():
    async with AsyncSessionLocal() as session:
        yield session

