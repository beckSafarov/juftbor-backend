# Database Models - Summary

## ✅ Completed Tasks

1. **Created organized folder structure** (`app/models/`)
2. **Implemented all 7 models** matching your production SQL schema
3. **Added all enums** for type safety
4. **Configured relationships** between models
5. **Added constraints and validation** matching SQL schema
6. **Maintained backward compatibility** with old `app/models.py`
7. **Updated database.py** with proper async session handling
8. **Updated init_db.py** to create all tables

## 📁 File Structure

```
app/
├── models/
│   ├── __init__.py          # Exports all models
│   ├── README.md            # Documentation
│   ├── enums.py             # 8 enum types
│   ├── user.py              # User model (main profile)
│   ├── interest.py          # Interest tracking
│   ├── metadata.py          # User metadata
│   ├── preferences.py       # Matchmaking preferences
│   ├── match.py             # Mutual matches
│   ├── photo.py             # Profile photos
│   └── report.py            # User reports
├── models.py                # Backward compatibility
├── database.py              # Database config
└── main.py                  # FastAPI app

init_db.py                   # Database initialization script
juftbor-db-production.sql    # SQL schema reference
```

## 🚀 Next Steps

### 1. Install Dependencies (if not already)
```bash
pip install fastapi uvicorn sqlalchemy asyncpg python-dotenv alembic
```

### 2. Configure Environment
Create `.env` file:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/juftbor
```

### 3. Initialize Database
```bash
python init_db.py
```

This will create all tables with:
- ✅ All constraints (CHECK, UNIQUE, FOREIGN KEY)
- ✅ All relationships
- ✅ Default values
- ✅ Indexes (commented out in SQL, but auto-created for PKs and UNIQUEs)

### 4. Use Models in FastAPI

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, Interest, GenderEnum

app = FastAPI()

@app.post("/users")
async def create_user(db: AsyncSession = Depends(get_db)):
    user = User(
        full_name="John Doe",
        birthdate="1995-01-15",
        gender=GenderEnum.MALE,
        reg_phone="+998901234567",
        telegram_id=123456789
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    return user
```

## 🎯 Key Features

### 1. Type Safety
All enums provide type safety and autocomplete in your IDE.

### 2. Relationships
Models automatically load related data:
```python
user = await db.get(User, 1)
print(user.metadata.bot_activated)  # Access metadata
print(user.preferences.age_range)    # Access preferences
print(len(user.photos))              # Count photos
```

### 3. Constraints
All database constraints are enforced:
- Age must be 18+
- Height: 100-250cm
- Degree: 0-3
- Religious level: 0-3
- No self-interests
- Unique telegram_id

### 4. Async Support
All models work with FastAPI's async/await pattern.

## 📊 Model Relationships

```
User (1) ─── (1) Metadata
User (1) ─── (1) Preferences
User (1) ─── (N) Photo
User (1) ─── (N) Interest (as sender)
User (1) ─── (N) Interest (as receiver)
User (1) ─── (N) Report (as reporter)
User (1) ─── (N) Report (as reported)

Interest (2) ─── (1) Match (when both accept)
```

## 🔍 Common Queries

See `app/models/README.md` for detailed examples of:
- Creating users
- Expressing interests
- Querying with filters
- Creating matches
- Managing photos

## ⚠️ Important Notes

1. **Telegram ID vs Username**
   - `telegram_id` (BIGINT): Immutable identifier from Telegram API
   - `telegram_username` (TEXT): Display only, can change

2. **Match Creation**
   - Always ensure `user1_id < user2_id` when creating matches
   - Or use a helper function to handle this automatically

3. **Cascading Deletes**
   - Deleting a user cascades to: metadata, preferences, photos, interests, reports received
   - Reports made set reporter_id to NULL (keeps history)

4. **Array Fields**
   - PostgreSQL-specific feature for multi-select preferences
   - Examples: `preferred_towns`, `marital_status` preferences

## 🛠️ Troubleshooting

If you see import errors:
```bash
pip install sqlalchemy asyncpg
```

If database connection fails:
```bash
# Check DATABASE_URL in .env
# Format: postgresql+asyncpg://user:password@host:port/database
```

If table creation fails:
```bash
# Check PostgreSQL is running
# Verify user has CREATE TABLE permissions
```
