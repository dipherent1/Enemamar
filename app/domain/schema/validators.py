import re
from typing import Optional, Dict, Any, List, Union
from uuid import UUID
from pydantic import ValidationError, validator, field_validator
from app.domain.schema.enums import UserRole, CourseStatus, PaymentStatus, LessonType, CourseFilterOption

class UserValidators:
    """Validation methods for user-related data"""
    
    @staticmethod
    def validate_phone_number(phone_number: str) -> str:
        """
        Validate Ethiopian phone number format.
        
        Accepts:
        - 09XXXXXXXX (10 digits starting with 09)
        - +251XXXXXXXXX (international format)
        
        Returns the validated phone number or raises ValueError.
        """
        # Ethiopian phone number patterns
        pattern1 = r'^09\d{8}$'  # 09XXXXXXXX format
        pattern2 = r'^\+251\d{9}$'  # +251XXXXXXXXX format
        
        if re.match(pattern1, phone_number) or re.match(pattern2, phone_number):
            return phone_number
        
        raise ValueError(
            "Invalid phone number format. Use 09XXXXXXXX or +251XXXXXXXXX format."
        )
    
    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        """
        Validate email format.
        
        Returns the validated email or raises ValueError.
        """
        if email is None:
            return None
            
        # Basic email pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return email
        
        raise ValueError("Invalid email format.")
    
    @staticmethod
    def validate_password(password: str) -> str:
        """
        Validate password strength.
        
        Requirements:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        
        Returns the validated password or raises ValueError.
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter.")
            
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter.")
            
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one digit.")
            
        return password
    
    @staticmethod
    def validate_role(role: Optional[str]) -> str:
        """
        Validate user role.
        
        Returns the validated role or raises ValueError.
        """
        if role is None:
            return UserRole.STUDENT.value
            
        try:
            return UserRole(role).value
        except ValueError:
            valid_roles = ", ".join(UserRole.list())
            raise ValueError(f"Invalid role. Valid roles are: {valid_roles}")

class CourseValidators:
    """Validation methods for course-related data"""
    
    @staticmethod
    def validate_price(price: float) -> float:
        """
        Validate course price.
        
        Requirements:
        - Must be non-negative
        
        Returns the validated price or raises ValueError.
        """
        if price < 0:
            raise ValueError("Price cannot be negative.")
            
        return price
    
    @staticmethod
    def validate_discount(discount: Optional[float]) -> float:
        """
        Validate course discount.
        
        Requirements:
        - Must be non-negative
        - Must be less than or equal to 100 (if percentage)
        
        Returns the validated discount or raises ValueError.
        """
        if discount is None:
            return 0.0
            
        if discount < 0:
            raise ValueError("Discount cannot be negative.")
            
        if discount > 100:
            raise ValueError("Discount percentage cannot exceed 100.")
            
        return discount
    
    @staticmethod
    def validate_tags(tags: Optional[List[str]]) -> Optional[List[str]]:
        """
        Validate course tags.
        
        Requirements:
        - Each tag must be non-empty
        - No duplicate tags
        
        Returns the validated tags or raises ValueError.
        """
        if tags is None:
            return None
            
        # Remove empty tags and duplicates
        cleaned_tags = list(set(tag.strip() for tag in tags if tag.strip()))
        
        if not cleaned_tags:
            return None
            
        return cleaned_tags
    
    @staticmethod
    def validate_course_status(status: Optional[str]) -> str:
        """
        Validate course status.
        
        Returns the validated status or raises ValueError.
        """
        if status is None:
            return CourseStatus.DRAFT.value
            
        try:
            return CourseStatus(status).value
        except ValueError:
            valid_statuses = ", ".join(CourseStatus.list())
            raise ValueError(f"Invalid status. Valid statuses are: {valid_statuses}")
    
    @staticmethod
    def validate_filter_option(filter_option: Optional[str]) -> Optional[str]:
        """
        Validate course filter option.
        
        Returns the validated filter option or raises ValueError.
        """
        if filter_option is None:
            return None
            
        try:
            return CourseFilterOption(filter_option).value
        except ValueError:
            valid_options = ", ".join(CourseFilterOption.list())
            raise ValueError(f"Invalid filter option. Valid options are: {valid_options}")

class LessonValidators:
    """Validation methods for lesson-related data"""
    
    @staticmethod
    def validate_duration(duration: int) -> int:
        """
        Validate lesson duration.
        
        Requirements:
        - Must be positive
        
        Returns the validated duration or raises ValueError.
        """
        if duration <= 0:
            raise ValueError("Duration must be positive.")
            
        return duration
    
    @staticmethod
    def validate_order(order: Optional[int]) -> int:
        """
        Validate lesson order.
        
        Requirements:
        - Must be positive
        
        Returns the validated order or raises ValueError.
        """
        if order is None:
            return 1
            
        if order <= 0:
            raise ValueError("Order must be positive.")
            
        return order
    
    @staticmethod
    def validate_lesson_type(lesson_type: Optional[str]) -> str:
        """
        Validate lesson type.
        
        Returns the validated lesson type or raises ValueError.
        """
        if lesson_type is None:
            return LessonType.VIDEO.value
            
        try:
            return LessonType(lesson_type).value
        except ValueError:
            valid_types = ", ".join(LessonType.list())
            raise ValueError(f"Invalid lesson type. Valid types are: {valid_types}")

class VideoValidators:
    """Validation methods for video-related data"""
    
    @staticmethod
    def validate_video_id(video_id: str) -> str:
        """
        Validate video ID.
        
        Requirements:
        - Must be non-empty
        
        Returns the validated video ID or raises ValueError.
        """
        if not video_id or not video_id.strip():
            raise ValueError("Video ID cannot be empty.")
            
        return video_id.strip()
    
    @staticmethod
    def validate_library_id(library_id: str) -> str:
        """
        Validate library ID.
        
        Requirements:
        - Must be non-empty
        
        Returns the validated library ID or raises ValueError.
        """
        if not library_id or not library_id.strip():
            raise ValueError("Library ID cannot be empty.")
            
        return library_id.strip()
    
    @staticmethod
    def validate_secret_key(secret_key: str) -> str:
        """
        Validate secret key.
        
        Requirements:
        - Must be non-empty
        
        Returns the validated secret key or raises ValueError.
        """
        if not secret_key or not secret_key.strip():
            raise ValueError("Secret key cannot be empty.")
            
        return secret_key.strip()
