"""
Preferences model for user matchmaking preferences.
Stores what kind of matches the user is looking for.
"""
from sqlalchemy import Column, Integer, Text, ARRAY, ForeignKey, CheckConstraint, func
from sqlalchemy.dialects.postgresql import INT4RANGE, TIMESTAMP, ENUM
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import MaritalStatusEnum


class Preferences(Base):
    """User matchmaking preferences"""
    __tablename__ = "preferences"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    age_range = Column(INT4RANGE, default="[18, 60]")
    height_range = Column(INT4RANGE, default="[140, 200]")
    marital_status = Column(ARRAY(ENUM(MaritalStatusEnum, name="marital_status_enum")))
    preferred_towns = Column(ARRAY(Text))
    preferred_languages = Column(ARRAY(Text))
    occupation_blacklist = Column(ARRAY(Text))
    religious_level = Column(ARRAY(Integer))  # Array of 0-3
    preferred_degree = Column(ARRAY(Integer))  # Array of 0-3
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="preferences")

    __table_args__ = (
        CheckConstraint(
            "lower(age_range) >= 18 AND upper(age_range) <= 100",
            name="check_age_range_valid"
        ),
        CheckConstraint(
            "lower(height_range) >= 100 AND upper(height_range) <= 250",
            name="check_height_range_valid"
        ),
    )

    def __repr__(self):
        return f"<Preferences(user_id={self.user_id}, age_range={self.age_range}, height_range={self.height_range})>"
