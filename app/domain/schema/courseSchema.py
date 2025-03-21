from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from app.domain.model.user import User
from app.domain.schema.authSchema import UserResponse
from datetime import datetime

class VideoInput(BaseModel):
    video_id: str = Field(..., min_length=1)
    library_id: str = Field(..., min_length=1)
    secret_key: str = Field(..., min_length=1)

class videoResponse(BaseModel):
    id: UUID
    video_id: str
    library_id: str
    secret_key: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class LessonInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    duration: int = Field(..., gt=0)
    order: int = Field(default=None)
    video: Optional[VideoInput] = Field(default=None)

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
    order: int 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    video: Optional[videoResponse] = Field(default=None)

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
    tags: Optional[List[str]] = Field(default=None, description="List of tags for the course")
    thumbnail_url: Optional[str] = Field(default=None, description="URL of the course thumbnail")
    price: float = Field(..., ge=0)
    discount: Optional[float] = Field(default=None, description="Special offer price")
    instructor_id: UUID = Field(..., description="UUID of the instructor")
    lessons: Optional[List[LessonInput]] = Field(default=None, description="List of lessons for the course")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Programming",
                "description": "Learn Python from scratch",
                "tags": ["Python", "Programming"],
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
    tags: Optional[List[str]]
    price: float
    discount: Optional[float] = None
    thumbnail_url: Optional[str] = None
    instructor_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    instructor: Optional[UserResponse] = Field(default=None)
    lessons: Optional[List[LessonResponse]] = Field(default=None)

    model_config = {
        "from_attributes": True
    }

class CourseAnalysisResponse(BaseModel):
    course_id: UUID
    view_count: int
    no_of_enrollments: int
    no_of_lessons: int
    revenue: float


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

class PaymentResponse(BaseModel):
    id: UUID
    tx_ref: str
    ref_id: str
    user_id: UUID
    course_id: UUID
    amount: float
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class PaymentData(BaseModel):
    tx_ref: str
    amount: float
    user_id: UUID
    course_id: UUID
    email: str
    first_name: str
    last_name: str
    title: str
    callback_url: str

class CallbackPayload(BaseModel):
    trx_ref: str
    ref_id: str
    status: str

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    page_size: int = Field(default=10, ge=1, le=100, description="Number of items per page")

class SearchParams(PaginationParams):
    search: Optional[str] = Field(
        default=None,
        description="Fuzzy search term"
    )
    filter: Optional[str] = Field(
        default=None,
        description="Filter term"
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

