from app.utils.exceptions.exceptions import ValidationError, DuplicatedError, NotFoundError, AuthError
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

def normalize_phone_number(phone: str) -> str:
    # Strip +251, 251, or 0 at the start
    return re.sub(r'^(?:\+251|251|0)', '', phone)

def format_phone_for_sending(phone: str, use_plus_prefix=True) -> str:
    if use_plus_prefix:
        return f'+251{normalize_phone_number(phone)}'
    else:
        return f'0{normalize_phone_number(phone)}'

class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def signUp(self, sign_up_data: signUp):
        # Validate and normalize phone number
        regex = r'^(?:\+251|0)?9\d{8}$'
        if not re.match(regex, sign_up_data.phone_number):
            raise ValidationError(detail="Invalid phone number")
        
        # Normalize phone number to raw form (e.g., 966934381)
        sign_up_data.phone_number = normalize_phone_number(sign_up_data.phone_number)
        # Set username if not provided
        if not sign_up_data.username:
            sign_up_data.username = sign_up_data.phone_number
        
        # Validate email format
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if sign_up_data.email and not re.match(regex, sign_up_data.email):
            raise ValidationError(detail="Invalid email")

        # Convert sign_up_data to User ORM object
        user_obj = User(**sign_up_data.model_dump(exclude_none=True))

        # Hash the password
        user_obj.password = hash_password(user_obj.password)

        # Check for duplicate entry using database constraints
        # Create user in repository and handle errors
        user, err = self.user_repo.create_user(user_obj)
        if err:
            if isinstance(err, ValueError):
                raise ValidationError(detail="Invalid email or phone number")
            if isinstance(err, IntegrityError):
                raise DuplicatedError(detail="User with this email or phone number already exists")
            raise ValidationError(detail="Failed to create user", data=str(err))
        if not user:
            raise ValidationError(detail="Failed to create user")
        
        user_response = UserResponse.model_validate(user, from_attributes=True)

        # Return response
        response = signUpResponse(detail="User created successfully", user=user_response)
        return response

    def login(self, login_data: login):
        print(login_data)
        # Fetch user by email or phone and handle repo errors
        if login_data.email:
            user, err = self.user_repo.get_user_by_email(login_data.email)
            if err:
                raise ValidationError(detail="Error fetching user by email", data=str(err))
        elif login_data.phone_number:
            login_data.phone_number = normalize_phone_number(login_data.phone_number)
            user, err = self.user_repo.get_user_by_phone(login_data.phone_number)
            if err:
                raise ValidationError(detail="Error fetching user by phone number", data=str(err))
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
        tokens, err = self.user_repo.login(token_data)
        if err:
            raise ValidationError(detail="Login failed", data=str(err))
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        # Convert SQLAlchemy User object to Pydantic Response Model
        user_response = UserResponse.model_validate(user)
        login_response = loginResponse(detail="Login successful", access_token=access_token, refresh_token= refresh_token, user=user_response)
        return login_response
    
    def logout(self,refresh_token):
        decoded_token = verify_refresh_token(refresh_token)
        user_id = decoded_token.get("id")
        result, err = self.user_repo.delete_refresh(user_id, refresh_token)
        if err:
            raise ValidationError(detail="Error deleting refresh token", data=str(err))
        if not result:
            raise NotFoundError(detail="Refresh token not found for logout")
        return {"detail": "Successfully logged out"}



    def refresh_token(self, refresh_token: str):
        #get user id
        decoded_token = verify_refresh_token(refresh_token)
        user_id = decoded_token.get("id")
        #get refresh token
        token_obj, err = self.user_repo.get_user_by_refresh(user_id, refresh_token)
        if err:
            raise ValidationError(detail="Error validating refresh token", data=str(err))
        if not token_obj:
            raise AuthError(detail="Invalid refresh token or session expired")
        token_data = tokenLoginData(id=user_id, role=decoded_token.get("role"))
        access_token = create_access_token(token_data.model_dump())
        return {"access_token": access_token}

    def send_otp(self, phone_number: str):
        print("Sending OTP to phone number:", phone_number)
        phone_number = format_phone_for_sending(phone_number)
        try:
            status_code, content = send_otp_sms(phone_number)
        except Exception as e:
            raise ValidationError(detail="Failed to send OTP", data=str(e))
        print("Sending OTP to phone number:", phone_number)
        
        if status_code == 200:  # Assuming 200 means success
            print("OTP sent successfully to:", phone_number)
            return {"detail": "OTP sent successfully", "status_code": status_code}
        else:
            raise ValidationError(detail="Failed to send OTP", data=str(e))

    def verify_otp(self, phone_number: str, code: str):
        print("Verifying OTP for phone number:", phone_number)
        print("OTP code:", code)
        formatted_phone_number = format_phone_for_sending(phone_number)
        try:
            status_code, content = verify_otp_sms(formatted_phone_number, code)
        except Exception as e:
            raise ValidationError(detail="Error verifying OTP via SMS provider", data=str(e))
        
        if status_code == 200:
            # Normalize phone number to raw form (e.g., 966934381)
            phone_number = normalize_phone_number(formatted_phone_number)
            # phone_number = re.sub(r'^(?:\+251|0)', '', phone_number)
                        
            # Activate the user
            print("Normalized phone number:", phone_number)
            user, err = self.user_repo.activate_user(None, phone_number)
            if err:
                raise ValidationError(detail="Error activating user after OTP", data=str(err))
            if not user:
                raise NotFoundError(detail="User with this phone number does not exist")
            
            return {"detail": "OTP verified successfully", "status_code": status_code}
        
        else:
            raise ValidationError(detail=f"Failed to verify OTP: {str(content)}")

        
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)