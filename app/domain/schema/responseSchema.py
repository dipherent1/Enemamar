from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Generic, TypeVar
from uuid import UUID
from datetime import datetime
from app.domain.schema.authSchema import UserResponse
from app.domain.schema.comment_review_schema import CommentResponse, ReviewResponse

# Generic type for paginated responses
T = TypeVar('T')

# Base response model
class BaseResponse(BaseModel):
    """Base response model with a detail message"""
    detail: str = Field(
        ...,
        description="Response message",
        examples=["Operation successful"]
    )

# Error response model
class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(
        ...,
        description="Error message",
        examples=["An error occurred"]
    )

# OTP response models
class OTPSendResponse(BaseResponse):
    """OTP send response model"""
    pass

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "OTP sent successfully"
            }
        }
    }

class OTPVerifyResponse(BaseResponse):
    """OTP verification response model"""
    status_code: int = Field(
        ...,
        description="HTTP status code",
        examples=[200]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "OTP verified successfully",
                "status_code": 200
            }
        }
    }

# Auth response models
class LogoutResponse(BaseResponse):
    """Logout response model"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Successfully logged out"
            }
        }
    }

class TokenRefreshResponse(BaseModel):
    """Token refresh response model"""
    access_token: str = Field(
        ...,
        description="New JWT access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    }


# Forget Password response models
class ForgetPasswordResponse(BaseResponse):
    """Forget password response model"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "OTP sent to your phone number for password reset"
            }
        }
    }


class PasswordResetOTPVerifyResponse(BaseResponse):
    """Password reset OTP verification response model"""
    status_code: int = Field(
        ...,
        description="HTTP status code",
        examples=[200]
    )
    reset_token: str = Field(
        ...,
        description="Password reset token (expires in 10 minutes)",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "OTP verified successfully for password reset",
                "status_code": 200,
                "reset_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    }


class PasswordResetResponse(BaseResponse):
    """Password reset response model"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Password reset successfully"
            }
        }
    }

# Generic paginated response
class PaginatedResponse(BaseResponse, Generic[T]):
    """Paginated response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="Response data containing items and pagination info"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Items retrieved successfully",
                "data": {
                    "items": [],
                    "total": 0,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 0
                }
            }
        }
    }

# Course response models
class CourseListResponse(PaginatedResponse):
    """Course list response model"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Courses retrieved successfully",
                "data": {
                    "courses": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Introduction to Python",
                            "description": "Learn Python from scratch",
                            "price": 99.99,
                            "instructor_id": "123e4567-e89b-12d3-a456-426614174001"
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 1
                }
            }
        }
    }

class CourseDetailResponse(BaseResponse):
    """Course detail response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="Course details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Course retrieved successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Introduction to Python",
                    "description": "Learn Python from scratch",
                    "price": 99.99,
                    "discount": 0.1,
                    "thumbnail_url": "https://example.com/thumbnail.jpg",
                    "instructor_id": "123e4567-e89b-12d3-a456-426614174001",
                    "instructor": {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "first_name": "John",
                        "last_name": "Doe"
                    },
                    "lessons": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174002",
                            "title": "Getting Started with Python",
                            "description": "Learn the basics of Python programming",
                            "duration": 30
                        }
                    ]
                }
            }
        }
    }

class EnrollmentResponse(BaseResponse):
    """Enrollment response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="Enrollment details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Course enrolled successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "course_id": "123e4567-e89b-12d3-a456-426614174002",
                    "enrolled_at": "2023-01-01T12:00:00Z"
                }
            }
        }
    }

# User response models
class UserProfileResponse(BaseResponse):
    """User profile response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="User profile details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "User profile retrieved successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "0912345678",
                    "role": "student",
                    "is_active": True,
                    "profile_picture": "https://example.com/profile.jpg",
                    "created_at": "2023-01-01T12:00:00Z",
                    "updated_at": "2023-01-02T12:00:00Z"
                }
            }
        }
    }

class UserUpdateResponse(BaseResponse):
    """User update response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="Updated user profile"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "User profile updated successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "johndoe_updated",
                    "email": "john.doe.updated@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "0912345678",
                    "role": "student",
                    "is_active": True
                }
            }
        }
    }

# Payment response models
class PaymentInitiateResponse(BaseResponse):
    """Payment initiation response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="Payment initiation details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Payment initiated",
                "data": {
                    "payment": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "tx_ref": "TX123456789",
                        "user_id": "123e4567-e89b-12d3-a456-426614174001",
                        "course_id": "123e4567-e89b-12d3-a456-426614174002",
                        "amount": 89.99,
                        "status": "pending"
                    },
                    "chapa_response": {
                        "status": "success",
                        "data": {
                            "checkout_url": "https://checkout.chapa.co/checkout/payment/123456"
                        }
                    }
                }
            }
        }
    }

class PaymentCallbackResponse(BaseResponse):
    """Payment callback response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="Payment callback details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Payment successful",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "course_id": "123e4567-e89b-12d3-a456-426614174002",
                    "enrolled_at": "2023-01-01T12:00:00Z"
                }
            }
        }
    }

# Lesson response models
class LessonListResponse(PaginatedResponse):
    """Lesson list response model"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Lessons retrieved successfully",
                "data": {
                    "lessons": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Getting Started with Python",
                            "description": "Learn the basics of Python programming",
                            "duration": 30,
                            "order": 1
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 1
                }
            }
        }
    }

class LessonDetailResponse(BaseResponse):
    """Lesson detail response model"""
    data: Dict[str, Any] = Field(
        ...,
        description="Lesson details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Lesson retrieved successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Getting Started with Python",
                    "description": "Learn the basics of Python programming",
                    "duration": 30,
                    "order": 1,
                    "video_url": "https://example.com/video.mp4",
                    "created_at": "2023-01-01T12:00:00Z",
                    "updated_at": "2023-01-02T12:00:00Z"
                }
            }
        }
    }

# Comment response models
class CommentListResponse(PaginatedResponse):
    """Comment list response model"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Comments retrieved successfully",
                "data": {
                    "comments": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "content": "This course is very informative!",
                            "user_id": "123e4567-e89b-12d3-a456-426614174001",
                            "course_id": "123e4567-e89b-12d3-a456-426614174002",
                            "created_at": "2023-01-01T12:00:00Z"
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 1
                }
            }
        }
    }

class CommentDetailResponse(BaseResponse):
    """Comment detail response model"""
    data: CommentResponse = Field(..., description="Comment details")

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Comment retrieved successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "content": "This course is very informative!",
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "course_id": "123e4567-e89b-12d3-a456-426614174002",
                    "created_at": "2023-01-01T12:00:00Z",
                    "updated_at": "2023-01-02T12:00:00Z"
                }
            }
        }
    }

# Review response models
class ReviewListResponse(PaginatedResponse):
    """Review list response model"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Reviews retrieved successfully",
                "data": {
                    "reviews": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "rating": 5,
                            "user_id": "123e4567-e89b-12d3-a456-426614174001",
                            "course_id": "123e4567-e89b-12d3-a456-426614174002",
                            "created_at": "2023-01-01T12:00:00Z"
                        }
                    ],
                    "average_rating": 4.5,
                    "total": 1,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 1
                }
            }
        }
    }

class ReviewDetailResponse(BaseResponse):
    """Review detail response model"""
    data: ReviewResponse = Field(..., description="Review details")

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Review retrieved successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "rating": 5,
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "course_id": "123e4567-e89b-12d3-a456-426614174002",
                    "created_at": "2023-01-01T12:00:00Z",
                    "updated_at": "2023-01-02T12:00:00Z"
                }
            }
        }
    }

# for example create course input
# {
#     "title": "Python Programming",
#     "price": 50,
#     "discount":0,
#     "description": "Learn Python from scratch",
#     "tags": ["Python", "Programming", "hehe"],
#     "instructor_id": "0c18d25a-dc77-4be7-af62-aea00717077e",
#     "thumbnail_url": "https://example.com/thumbnail.jpg",
#     "lessons": [
#         {
#             "title": "Introduction to Python",
#             "description": "Learn the basics of Python programming",
#             "duration": 30,
#             "order":1,
#             "video": {
#                 "library_id": "393657",
#                 "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
#                 "secret_key": "e92ea1ea-c032-4870-8792-d92366dbcb29"
#             }
#         }
#     ]
# }

# create course response
# {
#     "detail": "Course created successfully",
#     "data": {
#         "id": "9a05d7bb-757f-44b5-9a9a-84e1e8d038df",
#         "title": "Python Programming",
#         "description": "Learn Python from scratch",
#         "tags": [
#             "Python",
#             "Programming",
#             "hehe"
#         ],
#         "price": 50.0,
#         "discount": 0.0,
#         "thumbnail_url": "https://example.com/thumbnail.jpg",
#         "instructor_id": "0c18d25a-dc77-4be7-af62-aea00717077e",
#         "created_at": "2025-05-04T10:57:36.135791+03:00",
#         "updated_at": null,
#         "instructor": {
#             "id": "0c18d25a-dc77-4be7-af62-aea00717077e",
#             "username": "instructor",
#             "email": "instructor2@gmail.com",
#             "first_name": "instructor",
#             "last_name": "instructor",
#             "phone_number": "921417155",
#             "role": "instructor",
#             "is_active": false,
#             "profile_picture": null,
#             "created_at": "2025-05-03T22:33:37.259634+03:00",
#             "updated_at": "2025-05-03T22:33:37.259634+03:00"
#         },
#         "lessons": [
#             {
#                 "id": "8d854347-ba90-422d-901e-2752ba47a6f1",
#                 "title": "Introduction to Python",
#                 "description": "Learn the basics of Python programming",
#                 "duration": 30,
#                 "video_url": null,
#                 "order": 1,
#                 "created_at": "2025-05-04T10:57:36.144121+03:00",
#                 "updated_at": null,
#                 "video": {
#                     "id": "0b98bfd7-2460-4e08-a37c-725e14c497bb",
#                     "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
#                     "library_id": "393657",
#                     "secret_key": "gAAAAABoFx3wyLT5UwPjdYwbe_HJY4T0MmPzyq-BDPvkdoH-rZi1JlYvuN3fQH2sRFhH06tJaeyZUplI1hefW-VWmrcobjBUouW8B6njxpiN7WP4_2P5Q90BLeI5_mYt3OnF6WnPATO2",
#                     "created_at": "2025-05-04T10:57:36.152502+03:00",
#                     "updated_at": "2025-05-04T10:57:36.152502+03:00"
#                 }
#             }
#         ]
#     }
# }

# get lesson by id response
# {
#     "detail": "Lesson fetched successfully",
#     "data": {
#         "id": "8d854347-ba90-422d-901e-2752ba47a6f1",
#         "title": "Introduction to Python",
#         "description": "Learn the basics of Python programming",
#         "duration": 30,
#         "video_url": "https://iframe.mediadelivery.net/embed/393657/3e52de58-dc2b-4269-a0f5-f181f004964a?token=37430fd202c1738a588a156ae76278c4fd88ece01bea21cc47f2abf83e88ead5&expires=1746350479",
#         "order": 1,
#         "created_at": "2025-05-04T10:57:36.144121+03:00",
#         "updated_at": null,
#         "video": {
#             "id": "0b98bfd7-2460-4e08-a37c-725e14c497bb",
#             "video_id": "3e52de58-dc2b-4269-a0f5-f181f004964a",
#             "library_id": "393657",
#             "secret_key": "gAAAAABoFx3wyLT5UwPjdYwbe_HJY4T0MmPzyq-BDPvkdoH-rZi1JlYvuN3fQH2sRFhH06tJaeyZUplI1hefW-VWmrcobjBUouW8B6njxpiN7WP4_2P5Q90BLeI5_mYt3OnF6WnPATO2",
#             "created_at": "2025-05-04T10:57:36.152502+03:00",
#             "updated_at": "2025-05-04T10:57:36.152502+03:00"
#         }
#     }
# }