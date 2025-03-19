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
from app.utils.security.jwt_handler import verify_refresh_token, verify_access_token, create_access_token, create_refresh_token
from app.utils.otp.sms import send_otp_sms, verify_otp_sms

class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def signUp(self, sign_up_data: signUp):
        # Validate phone number
        regex = r'^(?:\+251|0)?9\d{8}$'
        if not re.match(regex, sign_up_data.phone_number):
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
        # user_response = UserResponse(
        #     id=user.id,
        #     username=user.username,
        #     first_name=user.first_name,
        #     last_name=user.last_name,
        #     email=user.email,
        #     phone_number=user.phone_number,
        #     role=user.role,
        #     is_active=user.is_active
        # )
        user_response = UserResponse.model_validate(user)

        # Return response
        response = signUpResponse(detail="User created successfully", user=user_response)
        return response

    def login(self, login_data: login):
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
        
        user_response = UserResponse.model_validate(user)
    #     user_data = {
    #     "id": user.id,
    #     "username": user.username,
    #     "email": user.email,
    #     "first_name": user.first_name,
    #     "last_name": user.last_name,
    #     "phone_number": user.phone_number,
    #     "role": user.role,
    #     "is_active": user.is_active,
    # }
        if not user.is_active:
            raise ValidationError(detail="User is not active")

        if not verify_password(login_data.password, user.password):
            raise ValidationError(detail="Incorrect password")
        
        # Create access token and refresh token
        token_data = tokenLoginData(id=user.id, role=user.role)
        access_token, refresh_token = self.user_repo.login(token_data)

        # Convert SQLAlchemy User object to Pydantic Response Model
        user_response = UserResponse.model_validate(user)
        login_response = loginResponse(detail="Login successful", access_token=access_token, refresh_token= refresh_token, user=user_response)
        return login_response
    
    def logout(self,refresh_token):
        decoded_token = verify_refresh_token(refresh_token)
        user_id = decoded_token.get("id")
        result = self.user_repo.delete_refresh(user_id,refresh_token)
        if not result:
            raise ValidationError(detail="Failed to logout, refresh token not found")



    def refresh_token(self, refresh_token: str):
        #get user id
        decoded_token = verify_refresh_token(refresh_token)
        user_id = decoded_token.get("id")
        #get refresh token
        user = self.user_repo.get_user_by_refresh(user_id, refresh_token)
        if not user:
            raise ValidationError(detail="Invalid refresh token, user has been logged out")
        token_data = tokenLoginData(id=user_id, role=decoded_token.get("role"))
        access_token = create_access_token(token_data.model_dump())
        return {"access_token": access_token}

    def send_otp(self, phone_number: str):
        status_code, content = send_otp_sms(phone_number)
        
        if status_code == 200:  # Assuming 200 means success
            return {"detail": "OTP sent successfully", "status_code": status_code}
        else:
            raise ValidationError(detail="Failed to send OTP", data=content)

    def verify_otp(self, phone_number: str, code: str):
        status_code, content = verify_otp_sms(phone_number, code)
        
        if status_code == 200:
            self.user_repo.verify_user(phone_number)
            return {"detail": "OTP verified successfully", "status_code": status_code}
        
        else:
            raise ValidationError(detail="Failed to verify OTP", data=content)

        
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)