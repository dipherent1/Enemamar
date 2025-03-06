from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from app.domain.model.user import User
from app.domain.schema.authSchema import UserResponse
from datetime import datetime

class LessonInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    duration: int = Field(..., gt=0)
    video_url: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming",
                "duration": 30,
                "video_url": "https://example.com/video.mp4"
            }
        }
    }

class LessonResponse(BaseModel):
    id: UUID
    title: str
    description: str
    duration: int
    video_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class MultipleLessonInput(BaseModel):
    lessons: List[LessonInput]

    model_config = {
        "json_schema_extra": {
            "example": {
                "lessons": [
                    {
                        "title": "Introduction to Python",
                        "description": "Learn the basics of Python programming",
                        "duration": 30,
                        "video_url": "https://example.com/video1.mp4"
                    },
                    {
                        "title": "Advanced Python",
                        "description": "Learn advanced Python concepts",
                        "duration": 45,
                        "video_url": "https://example.com/video2.mp4"
                    }
                ]
            }
        }
    }


class CourseInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    instructor_id: UUID = Field(..., description="UUID of the instructor")
    lessons: Optional[List[LessonInput]] = Field(default=None, description="List of lessons for the course")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Programming",
                "description": "Learn Python from scratch",
                "price": 99.99,
                "instructor_id": "123e4567-e89b-12d3-a456-426614174000",
                "lessons": [
                    {
                        "title": "Introduction to Python",
                        "description": "Learn the basics of Python programming",
                        "duration": 30,
                        "video_url": "https://example.com/video1.mp4"
                    }
                ]
            }
        }
    }

class CourseResponse(BaseModel):
    id: UUID
    title: str
    description: str
    price: float
    instructor_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    instructor: Optional[UserResponse] = None
    lessons: Optional[List[LessonResponse]] = None

    model_config = {
        "from_attributes": True
    }

class CreateCourseResponse(BaseModel):
    detail: str
    course: CourseResponse

class EnrollmentResponse(BaseModel):
    id: UUID
    user_id: UUID
    course_id: UUID
    enrolled_at: Optional[datetime] = None
    class Config:
        from_attributes = True 

class EnrollResponse(BaseModel):
    detail: str
    enrollment: EnrollmentResponse

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    page_size: int = Field(default=10, ge=1, le=100, description="Number of items per page")

class CourseSearchParams(PaginationParams):
    search: Optional[str] = Field(
        default=None,
        description="Fuzzy search term for course title and description"
    )

class ModuleInput(BaseModel):
    title: str
    description: str
    is_published: Optional[bool] = False

class ModuleResponse(BaseModel):
    id: UUID
    title: str
    description: str
    is_published: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

