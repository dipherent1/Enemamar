from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from uuid import UUID
from app.domain.schema.authSchema import UserResponse
from datetime import datetime
from app.domain.schema.enums import CourseStatus, CourseFilterOption, LessonType, PaymentStatus
from app.domain.schema.validators import CourseValidators, LessonValidators, VideoValidators

class VideoInput(BaseModel):
    """Video input schema for creating or updating video content"""
    video_id: str = Field(
        ...,
        min_length=1,
        description="Video ID from the video hosting service",
        examples=["3e52de58-dc2b-4269-a0f5-f181f004964a"]
    )
    library_id: str = Field(
        ...,
        min_length=1,
        description="Library ID from the video hosting service",
        examples=["393657"]
    )
    secret_key: str = Field(
        ...,
        min_length=1,
        description="Secret key for generating secure URLs",
        examples=["e92ea1ea-c032-4870-8792-d92366dbcb29"]
    )

    @field_validator('video_id')
    @classmethod
    def validate_video_id(cls, v):
        return VideoValidators.validate_video_id(v)

    @field_validator('library_id')
    @classmethod
    def validate_library_id(cls, v):
        return VideoValidators.validate_library_id(v)

    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v):
        return VideoValidators.validate_secret_key(v)

    model_config = {
        "json_schema_extra": {
            "example": {
                "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
                "library_id": "393657",
                "secret_key": "e92ea1ea-c032-4870-8792-d92366dbcb29"
            }
        }
    }

class videoResponse(BaseModel):
    """Video response schema for retrieving video content"""
    id: UUID = Field(
        ...,
        description="Unique identifier for the video",
        examples=["0b98bfd7-2460-4e08-a37c-725e14c497bb"]
    )
    video_id: str = Field(
        ...,
        description="Video ID from the video hosting service",
        examples=["3e52de58-dc2b-4269-a0f5-f181f004964a"]
    )
    library_id: str = Field(
        ...,
        description="Library ID from the video hosting service",
        examples=["393657"]
    )
    secret_key: str = Field(
        ...,
        description="Encrypted secret key for generating secure URLs",
        examples=["gAAAAABoFx3wyLT5UwPjdYwbe_HJY4T0MmPzyq-BDPvkdoH-rZi1JlYvuN3fQH2sRFhH06tJaeyZUplI1hefW-VWmrcobjBUouW8B6njxpiN7WP4_2P5Q90BLeI5_mYt3OnF6WnPATO2"]
    )
    lesson_id: Optional[UUID] = Field(
        None,
        description="ID of the associated lesson",
        examples=["8d854347-ba90-422d-901e-2752ba47a6f1"]
    )
    created_at: Optional[datetime] = Field(
        None,
        description="Creation timestamp",
        examples=["2023-01-01T12:00:00Z"]
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Last update timestamp",
        examples=["2023-01-02T12:00:00Z"]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "0b98bfd7-2460-4e08-a37c-725e14c497bb",
                "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
                "library_id": "393657",
                "secret_key": "gAAAAABoFx3wyLT5UwPjdYwbe_HJY4T0MmPzyq-BDPvkdoH-rZi1JlYvuN3fQH2sRFhH06tJaeyZUplI1hefW-VWmrcobjBUouW8B6njxpiN7WP4_2P5Q90BLeI5_mYt3OnF6WnPATO2",
                "lesson_id": "8d854347-ba90-422d-901e-2752ba47a6f1",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
    }

class LessonInput(BaseModel):
    """Lesson input schema for creating or updating lessons"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Lesson title",
        examples=["Introduction to Python"]
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Detailed lesson description",
        examples=["Learn the basics of Python programming including variables, data types, and control structures."]
    )
    duration: int = Field(
        ...,
        gt=0,
        description="Lesson duration in minutes",
        examples=[30]
    )
    order: int = Field(
        default=None,
        description="Order of the lesson in the course (1-based)",
        examples=[1]
    )
    lesson_type: Optional[str] = Field(
        default=LessonType.VIDEO.value,
        description=f"Type of lesson ({', '.join(LessonType.list())})",
        examples=[LessonType.VIDEO.value]
    )
    video: Optional[VideoInput] = Field(
        default=None,
        description="Video content information"
    )

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        return LessonValidators.validate_duration(v)

    @field_validator('order')
    @classmethod
    def validate_order(cls, v):
        return LessonValidators.validate_order(v)

    @field_validator('lesson_type')
    @classmethod
    def validate_lesson_type(cls, v):
        return LessonValidators.validate_lesson_type(v)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming including variables, data types, and control structures.",
                "duration": 30,
                "order": 1,
                "video": {
                    "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
                    "library_id": "393657",
                    "secret_key": "e92ea1ea-c032-4870-8792-d92366dbcb29"
                }
            }
        }
    }


class LessonResponse(BaseModel):
    """Lesson response schema for retrieving lesson information"""
    id: UUID = Field(
        ...,
        description="Unique identifier for the lesson",
        examples=["8d854347-ba90-422d-901e-2752ba47a6f1"]
    )
    title: str = Field(
        ...,
        description="Lesson title",
        examples=["Introduction to Python"]
    )
    description: str = Field(
        ...,
        description="Detailed lesson description",
        examples=["Learn the basics of Python programming including variables, data types, and control structures."]
    )
    duration: int = Field(
        ...,
        description="Lesson duration in minutes",
        examples=[30]
    )
    video_url: Optional[str] = Field(
        None,
        description="Generated secure video URL for playback",
        examples=["https://iframe.mediadelivery.net/embed/393657/3e52de58-dc2b-4269-a0f5-f181f004964a?token=37430fd202c1738a588a156ae76278c4fd88ece01bea21cc47f2abf83e88ead5&expires=1746350479"]
    )
    order: int = Field(
        ...,
        description="Order of the lesson in the course (1-based)",
        examples=[1]
    )
    course_id: Optional[UUID] = Field(
        None,
        description="ID of the course this lesson belongs to",
        examples=["9a05d7bb-757f-44b5-9a9a-84e1e8d038df"]
    )
    created_at: Optional[datetime] = Field(
        None,
        description="Creation timestamp",
        examples=["2023-01-01T12:00:00Z"]
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Last update timestamp",
        examples=["2023-01-02T12:00:00Z"]
    )
    video: Optional[videoResponse] = Field(
        default=None,
        description="Video content information"
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "8d854347-ba90-422d-901e-2752ba47a6f1",
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming",
                "duration": 30,
                "video_url": "https://iframe.mediadelivery.net/embed/393657/3e52de58-dc2b-4269-a0f5-f181f004964a?token=37430fd202c1738a588a156ae76278c4fd88ece01bea21cc47f2abf83e88ead5&expires=1746350479",
                "order": 1,
                "course_id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
    }

class MultipleLessonInput(BaseModel):
    """Input schema for adding multiple lessons to a course at once"""
    lessons: List[LessonInput] = Field(
        ...,
        description="List of lessons to add to the course",
        min_items=1
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "lessons": [
                    {
                        "title": "Introduction to Python",
                        "description": "Learn the basics of Python programming",
                        "duration": 30,
                        "order": 1,
                        "video": {
                            "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
                            "library_id": "393657",
                            "secret_key": "e92ea1ea-c032-4870-8792-d92366dbcb29"
                        }
                    },
                    {
                        "title": "Advanced Python",
                        "description": "Learn advanced Python concepts",
                        "duration": 45,
                        "order": 2,
                        "video": {
                            "video_id": "4f63ef59-ed3c-5370-b1f6-g292f115075b",
                            "library_id": "393657",
                            "secret_key": "f03fb2fb-d143-5981-9903-e03477dcb30a"
                        }
                    }
                ]
            }
        }
    }



class CourseInput(BaseModel):
    """Course input schema for creating or updating courses"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Course title",
        examples=["Python Programming Masterclass"]
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Detailed course description",
        examples=["A comprehensive course covering Python from basics to advanced topics including web development, data science, and automation."]
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="List of tags for categorizing the course",
        examples=[["Python", "Programming", "Web Development"]]
    )
    thumbnail_url: Optional[str] = Field(
        default=None,
        description="URL of the course thumbnail image",
        examples=["https://example.com/thumbnails/python-course.jpg"]
    )
    price: float = Field(
        ...,
        ge=0,
        description="Course price in USD",
        examples=[99.99]
    )
    discount: Optional[float] = Field(
        default=0.0,
        description="Discount amount or percentage",
        examples=[10.0]
    )
    status: Optional[str] = Field(
        default=CourseStatus.DRAFT.value,
        description=f"Course publication status ({', '.join(CourseStatus.list())})",
        examples=[CourseStatus.PUBLISHED.value]
    )
    instructor_id: UUID = Field(
        ...,
        description="UUID of the course instructor",
        examples=["0c18d25a-dc77-4be7-af62-aea00717077e"]
    )
    lessons: Optional[List[LessonInput]] = Field(
        default=None,
        description="List of lessons to include in the course"
    )

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        return CourseValidators.validate_price(v)

    @field_validator('discount')
    @classmethod
    def validate_discount(cls, v):
        return CourseValidators.validate_discount(v)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        return CourseValidators.validate_tags(v)

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        return CourseValidators.validate_course_status(v)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Programming Masterclass",
                "description": "A comprehensive course covering Python from basics to advanced topics.",
                "tags": ["Python", "Programming", "Web Development"],
                "thumbnail_url": "https://example.com/thumbnails/python-course.jpg",
                "price": 99.99,
                "discount": 10.0,
                "instructor_id": "0c18d25a-dc77-4be7-af62-aea00717077e",
                "lessons": [
                    {
                        "title": "Introduction to Python",
                        "description": "Learn the basics of Python programming",
                        "duration": 30,
                        "order": 1,
                        "video": {
                            "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
                            "library_id": "393657",
                            "secret_key": "e92ea1ea-c032-4870-8792-d92366dbcb29"
                        }
                    }
                ]
            }
        }
    }

class CourseResponse(BaseModel):
    """Course response schema for retrieving course information"""
    id: UUID = Field(
        ...,
        description="Unique identifier for the course",
        examples=["9a05d7bb-757f-44b5-9a9a-84e1e8d038df"]
    )
    title: str = Field(
        ...,
        description="Course title",
        examples=["Python Programming Masterclass"]
    )
    description: str = Field(
        ...,
        description="Detailed course description",
        examples=["A comprehensive course covering Python from basics to advanced topics."]
    )
    tags: Optional[List[str]] = Field(
        None,
        description="List of tags categorizing the course",
        examples=[["Python", "Programming", "Web Development"]]
    )
    price: float = Field(
        ...,
        description="Course price in USD",
        examples=[99.99]
    )
    discount: Optional[float] = Field(
        None,
        description="Discount amount or percentage",
        examples=[10.0]
    )
    thumbnail_url: Optional[str] = Field(
        None,
        description="URL of the course thumbnail image",
        examples=["https://example.com/thumbnails/python-course.jpg"]
    )
    instructor_id: UUID = Field(
        ...,
        description="UUID of the course instructor",
        examples=["0c18d25a-dc77-4be7-af62-aea00717077e"]
    )
    view_count: Optional[int] = Field(
        None,
        description="Number of times the course has been viewed",
        examples=[1250]
    )
    created_at: Optional[datetime] = Field(
        None,
        description="Creation timestamp",
        examples=["2023-01-01T12:00:00Z"]
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Last update timestamp",
        examples=["2023-01-02T12:00:00Z"]
    )
    instructor: Optional[UserResponse] = Field(
        default=None,
        description="Detailed information about the course instructor"
    )
    lessons: Optional[List[LessonResponse]] = Field(
        default=None,
        description="List of lessons included in the course"
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
                "title": "Python Programming Masterclass",
                "description": "A comprehensive course covering Python from basics to advanced topics.",
                "tags": ["Python", "Programming", "Web Development"],
                "price": 99.99,
                "discount": 10.0,
                "thumbnail_url": "https://example.com/thumbnails/python-course.jpg",
                "instructor_id": "0c18d25a-dc77-4be7-af62-aea00717077e",
                "view_count": 1250,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
    }

class CourseAnalysisResponse(BaseModel):
    """Response schema for course analytics data"""
    view_count: int = Field(
        ...,
        description="Number of times the course has been viewed",
        examples=[1250]
    )
    no_of_enrollments: int = Field(
        ...,
        description="Number of students enrolled in the course",
        examples=[85]
    )
    no_of_lessons: int = Field(
        ...,
        description="Total number of lessons in the course",
        examples=[12]
    )
    revenue: float = Field(
        ...,
        description="Total revenue generated by the course in USD",
        examples=[8499.15]
    )
    course: Optional[CourseResponse] = Field(
        default=None,
        description="Detailed course information"
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "view_count": 1250,
                "no_of_enrollments": 85,
                "no_of_lessons": 12,
                "revenue": 8499.15,
                "course": {
                    "id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
                    "title": "Python Programming Masterclass",
                    "description": "A comprehensive course covering Python from basics to advanced topics.",
                    "price": 99.99
                }
            }
        }
    }


class CreateCourseResponse(BaseModel):
    """Response schema for course creation"""
    detail: str = Field(
        ...,
        description="Response message",
        examples=["Course created successfully"]
    )
    course: CourseResponse = Field(
        ...,
        description="Created course details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Course created successfully",
                "course": {
                    "id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
                    "title": "Python Programming Masterclass",
                    "description": "A comprehensive course covering Python from basics to advanced topics.",
                    "price": 99.99
                }
            }
        }
    }

class EnrollmentResponse(BaseModel):
    """Response schema for course enrollment details"""
    id: UUID = Field(
        ...,
        description="Unique identifier for the enrollment",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    user_id: UUID = Field(
        ...,
        description="ID of the enrolled user",
        examples=["0c18d25a-dc77-4be7-af62-aea00717077e"]
    )
    course_id: UUID = Field(
        ...,
        description="ID of the course enrolled in",
        examples=["9a05d7bb-757f-44b5-9a9a-84e1e8d038df"]
    )
    enrolled_at: Optional[datetime] = Field(
        None,
        description="Enrollment timestamp",
        examples=["2023-01-01T12:00:00Z"]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "0c18d25a-dc77-4be7-af62-aea00717077e",
                "course_id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
                "enrolled_at": "2023-01-01T12:00:00Z"
            }
        }
    }

class EnrollResponse(BaseModel):
    """Response schema for course enrollment"""
    detail: str = Field(
        ...,
        description="Response message",
        examples=["Successfully enrolled in course"]
    )
    enrollment: EnrollmentResponse = Field(
        ...,
        description="Enrollment details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Successfully enrolled in course",
                "enrollment": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "user_id": "0c18d25a-dc77-4be7-af62-aea00717077e",
                    "course_id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
                    "enrolled_at": "2023-01-01T12:00:00Z"
                }
            }
        }
    }

class PaymentResponse(BaseModel):
    """Response schema for payment transaction details"""
    id: UUID = Field(
        ...,
        description="Unique identifier for the payment transaction",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    tx_ref: str = Field(
        ...,
        description="Transaction reference ID",
        examples=["tx-1234567890"]
    )
    ref_id: Optional[str] = Field(
        None,
        description="Payment provider reference ID",
        examples=["pay-9876543210"]
    )
    user_id: UUID = Field(
        ...,
        description="ID of the user making the payment",
        examples=["0c18d25a-dc77-4be7-af62-aea00717077e"]
    )
    course_id: UUID = Field(
        ...,
        description="ID of the course being purchased",
        examples=["9a05d7bb-757f-44b5-9a9a-84e1e8d038df"]
    )
    amount: float = Field(
        ...,
        description="Payment amount in USD",
        examples=[99.99]
    )
    status: str = Field(
        ...,
        description=f"Payment status ({', '.join(PaymentStatus.list())})",
        examples=[PaymentStatus.COMPLETED.value]
    )
    created_at: Optional[datetime] = Field(
        None,
        description="Payment creation timestamp",
        examples=["2023-01-01T12:00:00Z"]
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Payment last update timestamp",
        examples=["2023-01-01T12:05:30Z"]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "tx_ref": "tx-1234567890",
                "ref_id": "pay-9876543210",
                "user_id": "0c18d25a-dc77-4be7-af62-aea00717077e",
                "course_id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
                "amount": 99.99,
                "status": "completed",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:05:30Z"
            }
        }
    }

class PaymentData(BaseModel):
    """Input schema for initiating a payment"""
    amount: float = Field(
        ...,
        description="Payment amount in USD",
        examples=[99.99]
    )
    phone_number: str = Field(
        ...,
        description="User's phone number for payment notifications",
        examples=["0912345678"]
    )
    tx_ref: Optional[str] = Field(
        None,
        description="Transaction reference ID (generated if not provided)",
        examples=["tx-1234567890"]
    )
    user_id: Optional[UUID] = Field(
        None,
        description="ID of the user making the payment",
        examples=["0c18d25a-dc77-4be7-af62-aea00717077e"]
    )
    course_id: Optional[UUID] = Field(
        None,
        description="ID of the course being purchased",
        examples=["9a05d7bb-757f-44b5-9a9a-84e1e8d038df"]
    )
    email: Optional[str] = Field(
        None,
        description="User's email address for payment notifications",
        examples=["john.doe@example.com"]
    )
    first_name: Optional[str] = Field(
        None,
        description="User's first name",
        examples=["John"]
    )
    last_name: Optional[str] = Field(
        None,
        description="User's last name",
        examples=["Doe"]
    )
    title: Optional[str] = Field(
        None,
        description="Payment title or description",
        examples=["Purchase of Python Programming Masterclass"]
    )
    callback_url: Optional[str] = Field(
        None,
        description="URL to redirect after payment completion",
        examples=["https://example.com/payment/callback"]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "amount": 99.99,
                "phone_number": "0912345678",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "title": "Purchase of Python Programming Masterclass",
                "callback_url": "https://example.com/payment/callback"
            }
        }
    }

class CallbackPayload(BaseModel):
    """Payload schema for payment callback from payment provider"""
    trx_ref: str = Field(
        ...,
        description="Transaction reference ID",
        examples=["tx-1234567890"]
    )
    ref_id: str = Field(
        ...,
        description="Payment provider reference ID",
        examples=["pay-9876543210"]
    )
    status: str = Field(
        ...,
        description=f"Payment status ({', '.join(PaymentStatus.list())})",
        examples=[PaymentStatus.COMPLETED.value]
    )

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        try:
            return PaymentStatus(v).value
        except ValueError:
            # Map external payment provider status to our internal status
            status_mapping = {
                "success": PaymentStatus.COMPLETED.value,
                "failed": PaymentStatus.FAILED.value,
                "pending": PaymentStatus.PENDING.value
            }
            if v in status_mapping:
                return status_mapping[v]
            raise ValueError(f"Invalid payment status. Valid statuses are: {', '.join(PaymentStatus.list())}")

    model_config = {
        "json_schema_extra": {
            "example": {
                "trx_ref": "tx-1234567890",
                "ref_id": "pay-9876543210",
                "status": "success"
            }
        }
    }

class PaginationParams(BaseModel):
    """Base pagination parameters for list endpoints"""
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (1-based)",
        examples=[1]
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page",
        examples=[10]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "page_size": 10
            }
        }
    }

class SearchParams(PaginationParams):
    """Extended pagination parameters with search and filter options"""
    search: Optional[str] = Field(
        default=None,
        description="Search term for filtering results by title, description, etc.",
        examples=["python"]
    )
    filter: Optional[str] = Field(
        default=None,
        description=f"Filter term for sorting results ({', '.join(CourseFilterOption.list())})",
        examples=[CourseFilterOption.PRICE_LOW.value, CourseFilterOption.NEWEST.value]
    )

    @field_validator('filter')
    @classmethod
    def validate_filter(cls, v):
        return CourseValidators.validate_filter_option(v)

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "page_size": 10,
                "search": "python",
                "filter": "price_low"
            }
        }
    }


class ModuleInput(BaseModel):
    """Input schema for creating or updating modules"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Module title",
        examples=["Python Basics"]
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Module description",
        examples=["Fundamental concepts of Python programming"]
    )
    is_published: Optional[bool] = Field(
        default=False,
        description="Whether the module is published and visible to students",
        examples=[True]
    )
    status: Optional[str] = Field(
        default=CourseStatus.DRAFT.value,
        description=f"Module status ({', '.join(CourseStatus.list())})",
        examples=[CourseStatus.PUBLISHED.value]
    )

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        return CourseValidators.validate_course_status(v)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Basics",
                "description": "Fundamental concepts of Python programming",
                "is_published": True
            }
        }
    }

class ModuleResponse(BaseModel):
    """Response schema for module information"""
    id: UUID = Field(
        ...,
        description="Unique identifier for the module",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    title: str = Field(
        ...,
        description="Module title",
        examples=["Python Basics"]
    )
    description: str = Field(
        ...,
        description="Module description",
        examples=["Fundamental concepts of Python programming"]
    )
    is_published: bool = Field(
        ...,
        description="Whether the module is published and visible to students",
        examples=[True]
    )
    created_at: Optional[datetime] = Field(
        None,
        description="Creation timestamp",
        examples=["2023-01-01T12:00:00Z"]
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Last update timestamp",
        examples=["2023-01-02T12:00:00Z"]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Python Basics",
                "description": "Fundamental concepts of Python programming",
                "is_published": True,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
    }

class LessonEditInput(BaseModel):
    """Lesson edit input schema for updating lessons without video"""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Lesson title",
        examples=["Introduction to Python"]
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Detailed lesson description",
        examples=["Learn the basics of Python programming including variables, data types, and control structures."]
    )
    duration: Optional[int] = Field(
        default=None,
        gt=0,
        description="Lesson duration in minutes",
        examples=[30]
    )
    order: Optional[int] = Field(
        default=None,
        description="Order of the lesson in the course (1-based)",
        examples=[1]
    )
    lesson_type: Optional[str] = Field(
        default=None,
        description=f"Type of lesson ({', '.join(LessonType.list())})",
        examples=[LessonType.VIDEO.value]
    )

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        if v is not None:
            return LessonValidators.validate_duration(v)
        return v

    @field_validator('order')
    @classmethod
    def validate_order(cls, v):
        if v is not None:
            return LessonValidators.validate_order(v)
        return v

    @field_validator('lesson_type')
    @classmethod
    def validate_lesson_type(cls, v):
        if v is not None:
            return LessonValidators.validate_lesson_type(v)
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming including variables, data types, and control structures.",
                "duration": 30,
                "order": 1
            }
        }
    }

class VideoEditInput(BaseModel):
    """Video edit input schema for updating video content"""
    video_id: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Video ID from the video hosting service",
        examples=["3e52de58-dc2b-4269-a0f5-f181f004964a"]
    )
    library_id: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Library ID from the video hosting service",
        examples=["393657"]
    )
    secret_key: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Secret key for generating secure URLs",
        examples=["e92ea1ea-c032-4870-8792-d92366dbcb29"]
    )

    @field_validator('video_id')
    @classmethod
    def validate_video_id(cls, v):
        if v is not None:
            return VideoValidators.validate_video_id(v)
        return v

    @field_validator('library_id')
    @classmethod
    def validate_library_id(cls, v):
        if v is not None:
            return VideoValidators.validate_library_id(v)
        return v

    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v):
        if v is not None:
            return VideoValidators.validate_secret_key(v)
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
                "library_id": "393657",
                "secret_key": "e92ea1ea-c032-4870-8792-d92366dbcb29"
            }
        }
    }

class CourseEditInput(BaseModel):
    """Course edit input schema for updating courses without lessons"""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Course title",
        examples=["Python Programming Masterclass"]
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Detailed course description",
        examples=["A comprehensive course covering Python from basics to advanced topics."]
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="List of tags for categorizing the course",
        examples=[["Python", "Programming", "Web Development"]]
    )
    thumbnail_url: Optional[str] = Field(
        default=None,
        description="URL of the course thumbnail image",
        examples=["https://example.com/thumbnails/python-course.jpg"]
    )
    price: Optional[float] = Field(
        default=None,
        ge=0,
        description="Course price in USD",
        examples=[99.99]
    )
    discount: Optional[float] = Field(
        default=None,
        description="Discount amount or percentage",
        examples=[10.0]
    )
    status: Optional[str] = Field(
        default=None,
        description=f"Course publication status ({', '.join(CourseStatus.list())})",
        examples=[CourseStatus.PUBLISHED.value]
    )
    instructor_id: UUID = Field(
        ...,
        description="UUID of the course instructor",
        examples=["0c18d25a-dc77-4be7-af62-aea00717077e"]
    )

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            return CourseValidators.validate_price(v)
        return v

    @field_validator('discount')
    @classmethod
    def validate_discount(cls, v):
        if v is not None:
            return CourseValidators.validate_discount(v)
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        return CourseValidators.validate_tags(v)

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            return CourseValidators.validate_course_status(v)
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Programming Masterclass",
                "description": "A comprehensive course covering Python from basics to advanced topics.",
                "tags": ["Python", "Programming", "Web Development"],
                "thumbnail_url": "https://example.com/thumbnails/python-course.jpg",
                "price": 99.99,
                "discount": 10.0,
                "instructor_id": "0c18d25a-dc77-4be7-af62-aea00717077e"
            }
        }
    }

