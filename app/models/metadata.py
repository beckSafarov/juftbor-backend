"""
Metadata model for user metadata tracking.
Stores bot activation, device info, IP, and ban status.
"""
from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import INET, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base


class Metadata(Base):
    """User metadata including bot activation, IP, device, and ban status"""
    __tablename__ = "metadata"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    registration_ip = Column(INET)
    device = Column(Text)
    bot_activated = Column(Boolean, default=False)
    last_active_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_edited_at = Column(TIMESTAMP(timezone=True))
    notify_matches = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(Text)
    ban_date = Column(TIMESTAMP(timezone=True))

    # Relationship
    user = relationship("User", back_populates="metadata")

    def __repr__(self):
        return f"<Metadata(user_id={self.user_id}, bot_activated={self.bot_activated}, is_banned={self.is_banned})>"
