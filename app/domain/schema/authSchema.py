from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from app.domain.model.user import User
from datetime import datetime


class signUp(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: str
    first_name: str
    last_name: str
    phone_number: str
    role: str
    class Config:
        from_attributes = True 

class login(BaseModel):
    email: Optional[str] = None
    password: str
    phone_number: Optional[str] = None

    def validate(self):
        if not self.password:
            raise ValueError("Password must be provided.")
        if not self.email and not self.phone_number:
            raise ValueError("Either email or phone_number must be provided.")
        if self.email and self.phone_number:
            raise ValueError("Provide only one of email or phone_number, not both.")
    class Config:
        from_attributes = True 

class UserResponse(BaseModel):
    id: UUID
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: str
    last_name: str
    phone_number: str
    role: str
    is_active: bool
    profile_picture: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True 

#edit user schema
class editUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    class Config:
        from_attributes = True 

class signUpResponse(BaseModel):
    detail: str
    user: UserResponse
    
class loginResponse(BaseModel):
    detail: str
    access_token: str
    refresh_token: str
    user: UserResponse

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class tokenLoginData(BaseModel):
    id: UUID
    role: str

class UpdateRoleRequest(BaseModel):
    role: str