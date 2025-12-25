"""
Script to reset the database by dropping all tables and types.
USE WITH CAUTION - This deletes all data!
"""
import asyncio
from sqlalchemy import text
from app.database import engine


async def reset_database():
    """Drop all tables and ENUM types, then recreate them"""
    async with engine.begin() as conn:
        print("⚠️  Dropping all tables...")
        
        # Drop tables in correct order (respecting foreign keys)
        await conn.execute(text("DROP TABLE IF EXISTS reports CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS photos CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS matches CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS interests CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS preferences CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS metadata CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        
        print("⚠️  Dropping all ENUM types...")
        
        # Drop ENUM types
        await conn.execute(text("DROP TYPE IF EXISTS activity_status_enum CASCADE;"))
        await conn.execute(text("DROP TYPE IF EXISTS contact_person_enum CASCADE;"))
        await conn.execute(text("DROP TYPE IF EXISTS marital_status_enum CASCADE;"))
        await conn.execute(text("DROP TYPE IF EXISTS gender_enum CASCADE;"))
        
        print("✅ Database cleaned successfully!")
        print("\nNow run: python init_db.py")


if __name__ == "__main__":
    asyncio.run(reset_database())
