from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Dict, Any
from uuid import UUID
from app.domain.model.user import User
from datetime import datetime
from app.domain.schema.enums import UserRole
from app.domain.schema.validators import UserValidators


class signUp(BaseModel):
    """User registration schema"""
    email: Optional[str] = Field(
        None,
        description="User's email address",
        examples=["john.doe@example.com"]
    )

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        return UserValidators.validate_email(v)

    username: Optional[str] = Field(
        None,
        description="Unique username",
        examples=["johndoe"]
    )
    password: str = Field(
        ...,
        description="User's password (min 8 characters, must include uppercase, lowercase, and digit)",
        min_length=8,
        examples=["SecurePass123"]
    )

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        return UserValidators.validate_password(v)

    first_name: str = Field(
        ...,
        description="User's first name",
        examples=["John"]
    )
    last_name: str = Field(
        ...,
        description="User's last name",
        examples=["Doe"]
    )
    phone_number: str = Field(
        ...,
        description="User's phone number (format: 09XXXXXXXX or +251XXXXXXXXX)",
        examples=["0912345678", "+251912345678"]
    )

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        return UserValidators.validate_phone_number(v)

    role: Optional[str] = Field(
        default=UserRole.STUDENT.value,
        description=f"User role ({', '.join(UserRole.list())})",
        examples=[UserRole.STUDENT.value]
    )

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        return UserValidators.validate_role(v)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "username": "johndoe",
                "password": "securepassword123",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "0912345678",
                "role": "student"
            }
        }
    }

class login(BaseModel):
    """User login schema"""
    email: Optional[str] = Field(
        None,
        description="User's email address",
        examples=["john.doe@example.com"]
    )
    password: str = Field(
        ...,
        description="User's password",
        examples=["SecurePass123"]
    )
    phone_number: Optional[str] = Field(
        None,
        description="User's phone number (alternative to email)",
        examples=["0912345678", "+251912345678"]
    )

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            return UserValidators.validate_email(v)
        return v

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        if v is not None:
            return UserValidators.validate_phone_number(v)
        return v

    def validate(self):
        """Validate login credentials"""
        if not self.password:
            raise ValueError("Password must be provided.")
        if not self.email and not self.phone_number:
            raise ValueError("Either email or phone_number must be provided.")
        if self.email and self.phone_number:
            raise ValueError("Provide only one of email or phone_number, not both.")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "securepassword123"
            }
        }
    }

class UserResponse(BaseModel):
    """User profile response schema"""
    id: UUID = Field(
        ...,
        description="Unique user identifier",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    username: Optional[str] = Field(
        None,
        description="User's username",
        examples=["johndoe"]
    )
    email: Optional[str] = Field(
        None,
        description="User's email address",
        examples=["john.doe@example.com"]
    )
    first_name: str = Field(
        ...,
        description="User's first name",
        examples=["John"]
    )
    last_name: str = Field(
        ...,
        description="User's last name",
        examples=["Doe"]
    )
    phone_number: str = Field(
        ...,
        description="User's phone number",
        examples=["0912345678"]
    )
    role: str = Field(
        ...,
        description="User's role (student, instructor, admin)",
        examples=["student"]
    )
    profession: Optional[str] = Field(
        None,
        description="User's profession",
        examples=["Software Developer"]
    )
    is_active: bool = Field(
        ...,
        description="Whether the user account is active",
        examples=[True]
    )
    profile_picture: Optional[str] = Field(
        None,
        description="URL to user's profile picture",
        examples=["https://example.com/profile.jpg"]
    )
    created_at: Optional[datetime] = Field(
        None,
        description="Account creation timestamp",
        examples=["2023-01-01T12:00:00Z"]
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Last account update timestamp",
        examples=["2023-01-02T12:00:00Z"]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "0912345678",
                "role": "student",
                "profession": "Software Developer",
                "is_active": True,
                "profile_picture": "https://example.com/profile.jpg",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }
    }

class editUser(BaseModel):
    """User profile update schema"""
    username: Optional[str] = Field(
        None,
        description="New username",
        examples=["johndoe_updated"]
    )
    email: Optional[str] = Field(
        None,
        description="New email address",
        examples=["john.doe.updated@example.com"]
    )
    first_name: Optional[str] = Field(
        None,
        description="New first name",
        examples=["Johnny"]
    )
    last_name: Optional[str] = Field(
        None,
        description="New last name",
        examples=["Doe"]
    )
    phone_number: Optional[str] = Field(
        None,
        description="New phone number",
        examples=["0987654321"]
    )
    profession: Optional[str] = Field(
        None,
        description="User's profession",
        examples=["Software Developer"]
    )
    profile_picture: Optional[str] = Field(
        None,
        description="URL to user's profile picture",
        examples=["https://example.com/profile.jpg"]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "username": "johndoe_updated",
                "email": "john.doe.updated@example.com",
                "first_name": "Johnny",
                "last_name": "Doe",
                "phone_number": "0987654321",
                "profession": "Software Developer",
                "profile_picture": "https://example.com/profile.jpg"
            }
        }
    }

class signUpResponse(BaseModel):
    """User registration response schema"""
    detail: str = Field(
        ...,
        description="Response message",
        examples=["User created successfully"]
    )
    user: UserResponse = Field(
        ...,
        description="Created user details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "User created successfully",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "0912345678",
                    "role": "student",
                    "is_active": True
                }
            }
        }
    }

class loginResponse(BaseModel):
    """User login response schema"""
    detail: str = Field(
        ...,
        description="Response message",
        examples=["Login successful"]
    )
    access_token: str = Field(
        ...,
        description="JWT access token for API authorization",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    refresh_token: str = Field(
        ...,
        description="JWT refresh token for obtaining new access tokens",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    user: UserResponse = Field(
        ...,
        description="Logged in user details"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Login successful",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "0912345678",
                    "role": "student",
                    "is_active": True
                }
            }
        }
    }

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str = Field(
        ...,
        description="JWT access token for API authorization",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    refresh_token: str = Field(
        ...,
        description="JWT refresh token for obtaining new access tokens",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    }

class tokenLoginData(BaseModel):
    """Token payload schema"""
    id: UUID = Field(
        ...,
        description="User ID",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    role: str = Field(
        ...,
        description="User role",
        examples=["student", "instructor", "admin"]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "student"
            }
        }
    }

class UpdateRoleRequest(BaseModel):
    """Role update request schema"""
    role: str = Field(
        ...,
        description=f"New role to assign ({', '.join(UserRole.list())})",
        examples=[role for role in UserRole.list()]
    )

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        return UserValidators.validate_role(v)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "role": "instructor"
            }
        }
    }

class RefreshTokenRequest(BaseModel):
    """Token refresh request schema"""
    refresh_token: str = Field(
        ...,
        description="JWT refresh token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    }