from app.utils.exceptions.exceptions import ValidationError, DuplicatedError, NotFoundError
import re
from app.domain.schema.authSchema import signUp, UserResponse, login,loginResponse, signUpResponse, tokenLoginData
from app.domain.model.user import User
from app.repository.userRepo import UserRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from app.utils.security.hash import hash_password, verify_password


class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def signUp(self, sign_up_data: signUp):
        # Validate phone number
        if not sign_up_data.phone_number.isdigit():
            raise ValidationError(detail="Invalid phone number")
        
        # Set username if not provided
        if not sign_up_data.username:
            sign_up_data.username = sign_up_data.phone_number
        
        # Validate email format
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if sign_up_data.email and not re.match(regex, sign_up_data.email):
            raise ValidationError(detail="Invalid email")

        # Convert sign_up_data to User ORM object
        user = User(**sign_up_data.model_dump(exclude_none=True))

        #hash the password
        user.password = hash_password(user.password)

        # Check for duplicate entry using database constraints
        try:
            user = self.user_repo.create_user(user)
        # Handle wrong format of email or phone number
        except ValueError:
            raise ValidationError(detail="Invalid email or phone number")
        # Handle duplicate entry
        except IntegrityError:
            raise DuplicatedError(detail="User with this email or phone number already exists")

        # Convert SQLAlchemy User object to Pydantic Response Model
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            role=user.role,
            is_active=user.is_active
        )

        # Return response
        response = signUpResponse(detail="User created successfully", user=user_response)
        return response

    def login(self,login_data: login):
        print(login_data)
        user = None
        if login_data.email:
            try:
                user = self.user_repo.get_user_by_email(login_data.email)
            except NotFoundError:
                raise NotFoundError(detail="User with this email does not exist")
        
        elif login_data.phone_number:
            try:
                user = self.user_repo.get_user_by_phone(login_data.phone_number)
            except NotFoundError:
                raise NotFoundError(detail="User with this phone number does not exist")
        
        else:
            raise ValidationError(detail="Provide either email or phone number")
        
        # Check if user exists and is active
        if not user:
            raise NotFoundError(detail="User with this email or phone number does not exist")
        
        user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "role": user.role,
        "is_active": user.is_active,
    }
        if not user.is_active:
            raise ValidationError(detail="User is not active")

        if not verify_password(login_data.password, user.password):
            raise ValidationError(detail="Incorrect password")
        
        # Create access token and refresh token
        token_data = tokenLoginData(id=user.id, role=user.role)
        access_token, refresh_token = self.user_repo.login(token_data)

        # Convert SQLAlchemy User object to Pydantic Response Model
        user_response = UserResponse(**user_data)
        login_response = loginResponse(detail="Login successful", access_token=access_token, refresh_token= refresh_token, user=user_response)
        return login_response
    
    def refresh_token(self, access_token: str):
        #TODO: check if inactive
        print(access_token)
        pass

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)