from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config.database import Base
from sqlalchemy.dialects.postgresql import UUID  # For PostgreSQL
from app.domain.model.course import Enrollment, Course, Payment, Comment, Review
import uuid
from typing import List


class User(Base):
    __tablename__ = 'users'  # This defines the table name in PostgreSQL

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    profession: Mapped[str | None] = mapped_column(String(100), nullable=True)
    profile_picture: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # Use server_default for timestamp
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Automatically update timestamp
    )

    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")

    courses_taught: Mapped[List["Course"]] = relationship(
        "Course",
        back_populates="instructor",
        foreign_keys="Course.instructor_id"
    )

    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="user")

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user")

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True

    # update the role of the user
    def update_role(self, role: str) -> None:
        """Update the role of the user."""
        self.role = role

    def __repr__(self) -> str:
        """String representation of the User model."""
        return f"<User {self.phone_number}>"


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    # Relationship to User model
    user: Mapped["User"] = relationship(back_populates="refresh_tokens")


