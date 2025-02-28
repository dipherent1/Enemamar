# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# --------------------------
# Users & Authentication
# --------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)  # student, instructor, admin

    # Relationships
    courses_created = relationship("Course", back_populates="instructor")
    enrollments = relationship("Enrollment", back_populates="user")
    payments = relationship("PaymentTransaction", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    reviews = relationship("Review", back_populates="user")

# --------------------------
# Courses & Learning
# --------------------------
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    instructor_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    instructor = relationship("User", back_populates="courses_created")
    enrollments = relationship("Enrollment", back_populates="course")
    modules = relationship("Module", back_populates="course")
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="courses")
    reviews = relationship("Review", back_populates="course")

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    module_id = Column(Integer, ForeignKey("modules.id"))
    module = relationship("Module", back_populates="lessons")
    video = relationship("VideoContent", back_populates="lesson", uselist=False)
    progress = relationship("LessonProgress", back_populates="lesson")

class VideoContent(Base):
    __tablename__ = "video_content"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    bunny_cdn_url = Column(String)
    lesson = relationship("Lesson", back_populates="video")

# --------------------------
# Payments & Certificates
# --------------------------
class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    user = relationship("User", back_populates="payments")
    course = relationship("Course")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="subscription")

# --------------------------
# Progress & Reviews
# --------------------------
class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    enrollment = relationship("Enrollment", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    enrollment = relationship("Enrollment", back_populates="certificate")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    user = relationship("User", back_populates="reviews")
    course = relationship("Course", back_populates="reviews")

# --------------------------
# Categories
# --------------------------
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_category_id = Column(Integer, ForeignKey("categories.id"))
    courses = relationship("Course", back_populates="category")
    children = relationship("Category")  # Self-referential

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    # Relationships
    user = relationship("User", back_populates="enrollments")  # M:N (Student ↔ Courses)
    course = relationship("Course", back_populates="enrollments")  # M:N
    progress = relationship("LessonProgress", back_populates="enrollment")  # 1:M (Enrollment → Progress)
    certificate = relationship("Certificate", back_populates="enrollment", uselist=False)  # 1:1