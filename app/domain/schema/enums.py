from enum import Enum, auto
from typing import List, Dict, Any, Optional

class UserRole(str, Enum):
    """Enum for user roles in the system"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    
    @classmethod
    def list(cls) -> List[str]:
        """Return a list of all role values"""
        return [role.value for role in cls]
    
    @classmethod
    def description(cls) -> Dict[str, str]:
        """Return descriptions for each role"""
        return {
            cls.STUDENT.value: "Regular user who can enroll in courses",
            cls.INSTRUCTOR.value: "User who can create and manage courses",
            cls.ADMIN.value: "User with administrative privileges"
        }

class CourseStatus(str, Enum):
    """Enum for course publication status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    
    @classmethod
    def list(cls) -> List[str]:
        """Return a list of all status values"""
        return [status.value for status in cls]
    
    @classmethod
    def description(cls) -> Dict[str, str]:
        """Return descriptions for each status"""
        return {
            cls.DRAFT.value: "Course is in draft mode and not visible to students",
            cls.PUBLISHED.value: "Course is published and available for enrollment",
            cls.ARCHIVED.value: "Course is archived and no longer available for new enrollments"
        }

class PaymentStatus(str, Enum):
    """Enum for payment statuses"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    
    @classmethod
    def list(cls) -> List[str]:
        """Return a list of all payment status values"""
        return [status.value for status in cls]
    
    @classmethod
    def description(cls) -> Dict[str, str]:
        """Return descriptions for each payment status"""
        return {
            cls.PENDING.value: "Payment has been initiated but not yet completed",
            cls.COMPLETED.value: "Payment has been successfully completed",
            cls.FAILED.value: "Payment attempt failed",
            cls.REFUNDED.value: "Payment was completed but has been refunded"
        }

class LessonType(str, Enum):
    """Enum for lesson types"""
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    
    @classmethod
    def list(cls) -> List[str]:
        """Return a list of all lesson type values"""
        return [type.value for type in cls]
    
    @classmethod
    def description(cls) -> Dict[str, str]:
        """Return descriptions for each lesson type"""
        return {
            cls.VIDEO.value: "Video-based lesson with streaming content",
            cls.TEXT.value: "Text-based lesson with reading material",
            cls.QUIZ.value: "Interactive quiz to test knowledge",
            cls.ASSIGNMENT.value: "Practical assignment to be completed by student"
        }

class CourseFilterOption(str, Enum):
    """Enum for course filtering options"""
    NEWEST = "newest"
    OLDEST = "oldest"
    PRICE_LOW = "price_low"
    PRICE_HIGH = "price_high"
    MOST_POPULAR = "most_popular"
    HIGHEST_RATED = "highest_rated"
    
    @classmethod
    def list(cls) -> List[str]:
        """Return a list of all filter option values"""
        return [option.value for option in cls]
    
    @classmethod
    def description(cls) -> Dict[str, str]:
        """Return descriptions for each filter option"""
        return {
            cls.NEWEST.value: "Sort courses by newest first",
            cls.OLDEST.value: "Sort courses by oldest first",
            cls.PRICE_LOW.value: "Sort courses by price, lowest first",
            cls.PRICE_HIGH.value: "Sort courses by price, highest first",
            cls.MOST_POPULAR.value: "Sort courses by popularity (enrollment count)",
            cls.HIGHEST_RATED.value: "Sort courses by rating, highest first"
        }
