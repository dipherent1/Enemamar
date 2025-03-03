from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from app.domain.model.user import User
from datetime import datetime


class CourseInput(BaseModel):
    title: str
    price: float
    description: str

class CourseResponse(BaseModel):
    id: UUID
    title: str
    price: float
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True 

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



