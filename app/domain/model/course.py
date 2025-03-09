from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, ARRAY
from sqlalchemy.sql import func
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID  # For PostgreSQL
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.model import User

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True
    )
    title = Column(String)
    price = Column(Float)
    description = Column(String)
    tags = Column(ARRAY(String))
    instructor_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    thumbnail_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    view_count = Column(Integer, default=0)

    # Relationships
    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course")  # Changed from modules to lessons
    instructor: Mapped["User"] = relationship(
        "User", 
        back_populates="courses_taught",
        foreign_keys=[instructor_id]
    )


class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    course_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"))

    # Relationships
    user = relationship("User", back_populates="enrollments")  # M:N (Student ↔ Courses)
    course = relationship("Course", back_populates="enrollments")  # M:N

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    title: Mapped[str]
    description: Mapped[str]
    duration: Mapped[int]
    video_url: Mapped[Optional[str]]
    course_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="lessons")
    video = relationship("Video", back_populates="lesson", uselist=False)  # Changed to one-to-one

class Video(Base):
    __tablename__ = "videos"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True
    )
    title = Column(String)
    description = Column(String)
    duration = Column(Integer)
    
    library_id = Column(String)
    video_id = Column(String)
    secret_key = Column(String)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    lesson_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lessons.id"), unique=True)  # Added unique constraint
    lesson = relationship("Lesson", back_populates="video")  # Changed to one-to-one