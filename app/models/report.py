"""
Report model for user reports and moderation.
Allows users to report inappropriate behavior.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, ENUM
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import ActivityStatusEnum


class Report(Base):
    """User reports for moderation"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    reported_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(50), nullable=False)  # e.g., 'scam', 'harassment', 'fake_profile'
    description = Column(Text)
    status = Column(
        ENUM(ActivityStatusEnum, name="activity_status_enum"),
        default="p"  # a: active, p: pending, d: dismissed
    )
    admin_notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    resolved_at = Column(TIMESTAMP(timezone=True))

    # Relationships
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reports_made")
    reported_user = relationship("User", foreign_keys=[reported_id], back_populates="reports_received")

    def __repr__(self):
        return f"<Report(id={self.id}, category='{self.category}', status={self.status})>"
