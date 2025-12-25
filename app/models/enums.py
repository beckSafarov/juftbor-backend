"""
Database enums for Juftbor matchmaking app.
These match the PostgreSQL ENUM types defined in the database schema.
"""
import enum


class GenderEnum(str, enum.Enum):
    """User gender"""
    MALE = "M"
    FEMALE = "F"


class MaritalStatusEnum(str, enum.Enum):
    """User marital status"""
    SINGLE = "S"
    MARRIED = "M"
    DIVORCED = "D"
    WIDOWED = "W"


class ContactPersonEnum(str, enum.Enum):
    """Who to contact regarding the user"""
    SELF = "s"          # Self
    DAUGHTER = "d"      # Daughter
    MOTHER = "m"        # Mother
    BROTHER = "b"       # Brother
    OTHER = "o"         # Other relative/guardian


class ActivityStatusEnum(str, enum.Enum):
    """User account activity status"""
    ACTIVE = "a"        # Active
    PAUSED = "p"        # Paused
    DEACTIVATED = "d"   # Deactivated


class InterestStatusEnum(int, enum.Enum):
    """Status of expressed interest"""
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


class HabitsEnum(str, enum.Enum):
    """Smoking/drinking habits"""
    NEVER = "n"         # Never
    SOCIALLY = "s"      # Socially
    YES = "y"           # Yes


class EducationLevelEnum(int, enum.Enum):
    """Education degree level"""
    NO_DEGREE = 0
    BACHELOR = 1
    MASTER = 2
    DOCTORATE = 3


class ReligiousLevelEnum(int, enum.Enum):
    """Level of religiousness"""
    NOT_RELIGIOUS = 0
    SOMEWHAT = 1
    MODERATE = 2
    VERY_RELIGIOUS = 3
