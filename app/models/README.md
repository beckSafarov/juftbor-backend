# Database Models Documentation

## Structure

The database models are organized in the `app/models/` directory:

```
app/models/
├── __init__.py       # Exports all models and enums
├── enums.py          # Database enum types
├── user.py           # User model
├── interest.py       # Interest model
├── metadata.py       # Metadata model
├── preferences.py    # Preferences model
├── match.py          # Match model
├── photo.py          # Photo model
└── report.py         # Report model
```

## Usage

### Importing Models

```python
# Import all models at once
from app.models import User, Interest, Metadata, Preferences, Match, Photo, Report

# Import specific enums
from app.models import GenderEnum, MaritalStatusEnum, ActivityStatusEnum

# Import everything
from app.models import *
```

### Backward Compatibility

The old `app/models.py` file still works for backward compatibility:

```python
# This still works
from app.models import User, Interest
```

## Models Overview

### User
Main user profile with personal, professional, and contact information.

**Key fields:**
- `full_name`, `birthdate`, `gender`, `marital_status`
- `height`, `weight`, `biography`
- `degree`, `field_of_study`, `occupation`
- `religious_level`, `drinks`, `smokes`
- `telegram_id`, `telegram_username`, `contact_phone`

**Relationships:**
- `metadata`: One-to-one with Metadata
- `preferences`: One-to-one with Preferences
- `photos`: One-to-many with Photo
- `interests_sent`: One-to-many with Interest (as sender)
- `interests_received`: One-to-many with Interest (as receiver)

### Interest
Tracks when users express interest in each other.

**Key fields:**
- `sender_id`, `receiver_id`
- `status`: 0=Pending, 1=Accepted, 2=Rejected
- `created_at`, `responded_at`

### Metadata
User metadata including bot activation, IP, device, and ban status.

**Key fields:**
- `bot_activated`, `last_active_at`
- `is_banned`, `ban_reason`, `ban_date`
- `notify_matches`

### Preferences
User matchmaking preferences.

**Key fields:**
- `age_range`, `height_range`
- `marital_status` (array)
- `preferred_towns`, `preferred_languages`
- `religious_level`, `preferred_degree` (arrays)

### Match
Created when both users accept each other (mutual interest).

**Key fields:**
- `user1_id`, `user2_id`
- `matched_at`, `is_active`

**Note:** `user1_id` is always < `user2_id` for consistency.

### Photo
User profile photos with ordering support.

**Key fields:**
- `user_id`, `url`
- `is_primary`, `order`

### Report
User reports for moderation.

**Key fields:**
- `reporter_id`, `reported_id`
- `category`, `description`
- `status`, `admin_notes`

## Database Initialization

To create all tables:

```bash
python init_db.py
```

This will:
1. Connect to the database using `DATABASE_URL` from `.env`
2. Create all tables with proper constraints
3. Set up all relationships

## Enums

All enums are defined in `app/models/enums.py`:

- `GenderEnum`: M, F
- `MaritalStatusEnum`: S (Single), M (Married), D (Divorced), W (Widowed)
- `ContactPersonEnum`: s (Self), d (Daughter), m (Mother), b (Brother), o (Other)
- `ActivityStatusEnum`: a (Active), p (Paused), d (Deactivated)
- `InterestStatusEnum`: 0 (Pending), 1 (Accepted), 2 (Rejected)
- `HabitsEnum`: n (Never), s (Socially), y (Yes)
- `EducationLevelEnum`: 0-3 (No degree to Doctorate)
- `ReligiousLevelEnum`: 0-3 (Not religious to Very religious)

## Example Queries

### Create a new user
```python
from app.models import User, GenderEnum, MaritalStatusEnum
from app.database import async_session

async def create_user():
    async with async_session() as session:
        user = User(
            full_name="John Doe",
            birthdate="1995-01-15",
            gender=GenderEnum.MALE,
            marital_status=MaritalStatusEnum.SINGLE,
            reg_phone="+998901234567",
            telegram_id=123456789
        )
        session.add(user)
        await session.commit()
        return user
```

### Query users with preferences
```python
from app.models import User
from sqlalchemy import select

async def get_users_with_preferences():
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.is_active == "a")
        )
        users = result.scalars().all()
        return users
```

### Express interest
```python
from app.models import Interest

async def express_interest(sender_id: int, receiver_id: int):
    async with async_session() as session:
        interest = Interest(
            sender_id=sender_id,
            receiver_id=receiver_id,
            status=0  # Pending
        )
        session.add(interest)
        await session.commit()
        return interest
```

## Constraints & Validation

All models include proper constraints:

- **Check constraints** for valid value ranges
- **Unique constraints** to prevent duplicates
- **Foreign key constraints** with cascade rules
- **NOT NULL constraints** for required fields

Example constraints:
- Age must be 18+
- Height between 100-250cm
- Degree level 0-3
- Religious level 0-3
- Users can't express interest in themselves

## Notes

- All timestamps are timezone-aware (TIMESTAMPTZ)
- Arrays are used for multi-select preferences (PostgreSQL feature)
- INT4RANGE is used for age/height ranges
- INET type is used for IP addresses
- All models use async SQLAlchemy for FastAPI compatibility
