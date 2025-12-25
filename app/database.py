from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine with echo for debugging (disable in production)
engine = create_async_engine(DATABASE_URL, echo=True)

# Declarative base for all models
Base = declarative_base()

# Async session factory
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)


# Dependency for FastAPI routes
async def get_db():
    """
    Dependency that provides a database session to route handlers.
    Usage in FastAPI routes:
    
    @app.get("/users")
    async def get_users(db: AsyncSession = Depends(get_db)):
        ...
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
