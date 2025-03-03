from pydantic import BaseModel, EmailStr
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



