import asyncio
from app.database import engine, Base
# Import all models so Base.metadata has all tables
from app.models import User, Interest, Metadata, Preferences, Match, Photo, Report


async def init():
    """Initialize database by creating all tables"""
    async with engine.begin() as conn:
        # Drop all tables (use with caution in production!)
        # print("⚠️  Dropping all existing tables...")
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        print("📝 Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init())
