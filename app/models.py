"""
DEPRECATED: Import models from app.models instead.
This file is kept for backward compatibility.
"""
from app.models import *  # noqa: F401, F403

# Backward compatibility
__all__ = [
    "GenderEnum",
    "MaritalStatusEnum",
    "ContactPersonEnum",
    "ActivityStatusEnum",
    "InterestStatusEnum",
    "HabitsEnum",
    "EducationLevelEnum",
    "ReligiousLevelEnum",
    "User",
    "Interest",
    "Metadata",
    "Preferences",
    "Match",
    "Photo",
    "Report",
]