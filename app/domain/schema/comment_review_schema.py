from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# Comment schemas
class CommentInput(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Comment content")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "This course is very informative and well-structured!"
            }
        }
    }

class CommentResponse(BaseModel):
    id: UUID
    content: str
    user_id: UUID
    course_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }

# Review schemas
class ReviewInput(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "rating": 5
            }
        }
    }

class ReviewResponse(BaseModel):
    id: UUID
    rating: int
    user_id: UUID
    course_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }

# Combined schemas for course details with comments and reviews
class CourseCommentResponse(BaseModel):
    comments: List[CommentResponse]
    
    model_config = {
        "from_attributes": True
    }

class CourseReviewResponse(BaseModel):
    reviews: List[ReviewResponse]
    average_rating: float
    
    model_config = {
        "from_attributes": True
    }
