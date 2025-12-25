"""
Photo model for user profile photos.
Supports multiple photos per user with ordering.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base


class Photo(Base):
    """User profile photos"""
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    order = Column(Integer, default=0)

    # Relationship
    user = relationship("User", back_populates="photos")

    def __repr__(self):
        return f"<Photo(id={self.id}, user_id={self.user_id}, is_primary={self.is_primary})>"
