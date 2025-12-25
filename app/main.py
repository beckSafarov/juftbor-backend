from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse

app = FastAPI(
    title="Juftbor API",
    description="Muslim matchmaking app for Uzbek market",
    version="1.0.0"
)


@app.get("/")
def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "Juftbor API is running"}


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user profile.
    
    Args:
        user_data: User information matching UserCreate schema
        db: Database session (injected by FastAPI)
    
    Returns:
        Created user with ID
    
    Raises:
        HTTPException 400: If validation fails or user already exists
        HTTPException 500: If database error occurs
    """
    try:
        # Check if user with same phone already exists
        result = await db.execute(
            select(User).where(User.reg_phone == user_data.reg_phone)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with phone {user_data.reg_phone} already exists"
            )
        
        # Check if telegram_id is already taken (if provided)
        if user_data.telegram_id:
            result = await db.execute(
                select(User).where(User.telegram_id == user_data.telegram_id)
            )
            existing_telegram = result.scalar_one_or_none()
            
            if existing_telegram:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User with telegram_id {user_data.telegram_id} already exists"
                )
        
        # Create new user
        new_user = User(**user_data.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user
    
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a user by ID.
    
    Args:
        user_id: User's ID
        db: Database session
    
    Returns:
        User information
    
    Raises:
        HTTPException 404: If user not found
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return user


@app.get("/users", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    List all users with pagination.
    
    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10, max: 100)
        db: Database session
    
    Returns:
        List of users
    """
    if limit > 100:
        limit = 100
    
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    
    return users
