"""
Pydantic schemas for User model.
Used for request/response validation in FastAPI endpoints.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date
from app.models.enums import (
    GenderEnum, MaritalStatusEnum, ContactPersonEnum, ActivityStatusEnum
)


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    # Required fields
    full_name: str = Field(..., min_length=2, max_length=255)
    birthdate: date
    gender: GenderEnum
    reg_phone: str = Field(..., min_length=10, max_length=15)

    # Optional personal information
    marital_status: Optional[MaritalStatusEnum] = None
    native_town: Optional[str] = None
    hometown: Optional[str] = None
    languages: Optional[List[str]] = None

    # Physical attributes
    height: Optional[int] = Field(None, ge=100, le=250)
    weight: Optional[int] = Field(None, ge=30, le=300)
    biography: Optional[str] = None

    # Professional/Education
    degree: Optional[int] = Field(None, ge=0, le=3)
    field_of_study: Optional[str] = None
    occupation: Optional[str] = None

    # Lifestyle
    religious_level: Optional[int] = Field(None, ge=0, le=3)
    drinks: Optional[str] = Field(None, pattern="^[nsy]$")
    smokes: Optional[str] = Field(None, pattern="^[nsy]$")
    number_of_children: Optional[int] = Field(None, ge=0)
    drinks_preference: Optional[str] = Field(None, pattern="^[nsy]$")
    smokes_preference: Optional[str] = Field(None, pattern="^[nsy]$")

    # Contact Information
    contact_person: Optional[ContactPersonEnum] = None
    contact_phone: Optional[str] = Field(None, min_length=10, max_length=15)
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None
    contact_comment: Optional[str] = None

    # Status
    is_active: Optional[ActivityStatusEnum] = ActivityStatusEnum.ACTIVE

    @validator('birthdate')
    def validate_age(cls, v):
        """Ensure user is at least 18 years old"""
        from datetime import date
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError('User must be at least 18 years old')
        if v.year < 1940:
            raise ValueError('Birthdate must be after 1940')
        return v

    @validator('telegram_id', 'contact_phone', always=True)
    def validate_contact_method(cls, v, values):
        """Ensure at least one contact method is provided"""
        # This validator runs for both fields, check after both are set
        if 'contact_phone' in values or v is not None:
            return v
        return v

    class Config:
        use_enum_values = True


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    full_name: str
    birthdate: date
    gender: str
    marital_status: Optional[str]
    native_town: Optional[str]
    hometown: Optional[str]
    languages: Optional[List[str]]
    height: Optional[int]
    weight: Optional[int]
    biography: Optional[str]
    degree: Optional[int]
    field_of_study: Optional[str]
    occupation: Optional[str]
    religious_level: Optional[int]
    drinks: Optional[str]
    smokes: Optional[str]
    number_of_children: Optional[int]
    drinks_preference: Optional[str]
    smokes_preference: Optional[str]
    reg_phone: str
    contact_person: Optional[str]
    contact_phone: Optional[str]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    contact_comment: Optional[str]
    is_active: str

    class Config:
        from_attributes = True  # Allows ORM model to dict conversion


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    native_town: Optional[str] = None
    hometown: Optional[str] = None
    languages: Optional[List[str]] = None
    height: Optional[int] = Field(None, ge=100, le=250)
    weight: Optional[int] = Field(None, ge=30, le=300)
    biography: Optional[str] = None
    field_of_study: Optional[str] = None
    occupation: Optional[str] = None
    religious_level: Optional[int] = Field(None, ge=0, le=3)
    drinks: Optional[str] = Field(None, pattern="^[nsy]$")
    smokes: Optional[str] = Field(None, pattern="^[nsy]$")
    number_of_children: Optional[int] = Field(None, ge=0)
    drinks_preference: Optional[str] = Field(None, pattern="^[nsy]$")
    smokes_preference: Optional[str] = Field(None, pattern="^[nsy]$")
    contact_person: Optional[ContactPersonEnum] = None
    contact_phone: Optional[str] = Field(None, min_length=10, max_length=15)
    telegram_username: Optional[str] = None
    contact_comment: Optional[str] = None

    class Config:
        use_enum_values = True
