"""
Database models for Juftbor matchmaking app.
All models are exported from this module for easy imports.
"""
from app.models.enums import (
    GenderEnum,
    MaritalStatusEnum,
    ContactPersonEnum,
    ActivityStatusEnum,
    InterestStatusEnum,
    HabitsEnum,
    EducationLevelEnum,
    ReligiousLevelEnum
)
from app.models.user import User
from app.models.interest import Interest
from app.models.metadata import Metadata
from app.models.preferences import Preferences
from app.models.match import Match
from app.models.photo import Photo
from app.models.report import Report

__all__ = [
    # Enums
    "GenderEnum",
    "MaritalStatusEnum",
    "ContactPersonEnum",
    "ActivityStatusEnum",
    "InterestStatusEnum",
    "HabitsEnum",
    "EducationLevelEnum",
    "ReligiousLevelEnum",
    # Models
    "User",
    "Interest",
    "Metadata",
    "Preferences",
    "Match",
    "Photo",
    "Report",
]
