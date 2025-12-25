"""
User model for Juftbor matchmaking app.
Contains main user profile information.
"""
from sqlalchemy import (
    Column, Integer, String, Date, Text, ARRAY, 
    CheckConstraint, func, BIGINT
)
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import (
    GenderEnum, MaritalStatusEnum, ContactPersonEnum, 
    ActivityStatusEnum, HabitsEnum
)


class User(Base):
    """Main user profile with personal and professional information"""
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Personal Information
    full_name = Column(String(255), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(
        ENUM(
            GenderEnum,
            name="gender_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    marital_status = Column(
        ENUM(
            MaritalStatusEnum,
            name="marital_status_enum",
            values_callable=lambda x: [e.value for e in x],
        )
    )
    native_town = Column(Text)
    hometown = Column(Text)
    languages = Column(ARRAY(Text))

    # Physical Attributes
    height = Column(Integer)  # in cm
    weight = Column(Integer)  # in kg
    biography = Column(Text)

    # Professional/Education
    degree = Column(Integer)  # 0-3: no degree, bachelor, master, doctorate
    field_of_study = Column(Text)
    occupation = Column(Text)

    # Lifestyle
    religious_level = Column(Integer)  # 0-3: not religious to very religious
    drinks = Column(String(1))  # 'n': never, 's': socially, 'y': yes
    smokes = Column(String(1))  # 'n': never, 's': socially, 'y': yes

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Contact Information
    reg_phone = Column(String(15), unique=True, nullable=False)  # Registration phone
    contact_person = Column(
        ENUM(
            ContactPersonEnum,
            name="contact_person_enum",
            values_callable=lambda x: [e.value for e in x],
        )
    )
    contact_phone = Column(String(15))  # Contact phone (may differ from reg_phone)
    telegram_id = Column(BIGINT, unique=True)  # Immutable Telegram user ID
    telegram_username = Column(Text)  # Display only, can change
    contact_comment = Column(Text)

    # Status
    is_active = Column(
        ENUM(
            ActivityStatusEnum,
            name="activity_status_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        server_default="a",
    )

    # Relationships
    user_metadata = relationship(
        "Metadata", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    preferences = relationship("Preferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    photos = relationship("Photo", back_populates="user", cascade="all, delete-orphan")

    # Interests sent and received
    interests_sent = relationship(
        "Interest", 
        foreign_keys="Interest.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan"
    )
    interests_received = relationship(
        "Interest", 
        foreign_keys="Interest.receiver_id",
        back_populates="receiver",
        cascade="all, delete-orphan"
    )

    # Reports
    reports_made = relationship(
        "Report",
        foreign_keys="Report.reporter_id",
        back_populates="reporter"
    )
    reports_received = relationship(
        "Report",
        foreign_keys="Report.reported_id",
        back_populates="reported_user",
        cascade="all, delete-orphan"
    )

    # Table Constraints
    __table_args__ = (
        # At least one contact method required
        CheckConstraint(
            "(contact_phone IS NOT NULL) OR (telegram_id IS NOT NULL)",
            name="check_contact_info_exists"
        ),
        # Validate drinks value
        CheckConstraint(
            "drinks IN ('n', 's', 'y') OR drinks IS NULL",
            name="check_drinks_value"
        ),
        # Validate smokes value
        CheckConstraint(
            "smokes IN ('n', 's', 'y') OR smokes IS NULL",
            name="check_smokes_value"
        ),
        # Validate degree range
        CheckConstraint(
            "(degree BETWEEN 0 AND 3) OR degree IS NULL",
            name="check_degree_range"
        ),
        # Validate religious level range
        CheckConstraint(
            "(religious_level BETWEEN 0 AND 3) OR religious_level IS NULL",
            name="check_religious_level_range"
        ),
        # Validate height
        CheckConstraint(
            "(height BETWEEN 100 AND 250) OR height IS NULL",
            name="check_height_reasonable"
        ),
        # Validate weight
        CheckConstraint(
            "(weight BETWEEN 30 AND 300) OR weight IS NULL",
            name="check_weight_reasonable"
        ),
        # Validate birthdate (18+ years old, not before 1940)
        CheckConstraint(
            "birthdate >= '1940-01-01' AND birthdate <= CURRENT_DATE - INTERVAL '18 years'",
            name="check_birthdate_valid"
        ),
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.full_name}', gender={self.gender})>"

    @property
    def age(self):
        """Calculate age from birthdate"""
        from datetime import date
        today = date.today()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )
