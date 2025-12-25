"""
Match model for mutual interests.
Created when both users accept each other's interest.
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, CheckConstraint, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base


class Match(Base):
    """Created when both users accept each other (mutual interest)"""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    matched_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="unique_match_pair"),
        CheckConstraint("user1_id < user2_id", name="check_user_order"),
    )

    def __repr__(self):
        return f"<Match(id={self.id}, user1={self.user1_id}, user2={self.user2_id}, active={self.is_active})>"
