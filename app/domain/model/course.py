from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID  # For PostgreSQL
from typing import Optional

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

    # Relationships
    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course")  # Changed from modules to lessons


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
    videos = relationship("Video", back_populates="lesson")  # 1:N (Lesson ↔ Videos)

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
    video_url = Column(String)
    duration = Column(Integer)
    is_published = Column(Boolean, default=False)
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
    lesson_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lessons.id"))
    lesson = relationship("Lesson", back_populates="videos")  # 1:N (Lesson ↔ Videos)