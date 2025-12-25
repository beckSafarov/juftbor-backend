"""
Interest model for tracking user interactions.
Records when users express interest in each other.
"""
from sqlalchemy import Column, Integer, CheckConstraint, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base


class Interest(Base):
    """Tracks when users express interest in each other"""
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Integer, default=0)  # 0: Pending, 1: Accepted, 2: Rejected
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    responded_at = Column(TIMESTAMP(timezone=True))

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="interests_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="interests_received")

    __table_args__ = (
        UniqueConstraint("sender_id", "receiver_id", name="unique_sender_receiver"),
        CheckConstraint("sender_id != receiver_id", name="check_no_self_interest"),
    )

    def __repr__(self):
        return f"<Interest(id={self.id}, sender={self.sender_id}, receiver={self.receiver_id}, status={self.status})>"
