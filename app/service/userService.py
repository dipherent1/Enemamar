from app.utils.exceptions.exceptions import ValidationError, DuplicatedError, NotFoundError
import re
from app.domain.schema.authSchema import signUp, UserResponse, login,loginResponse, signUpResponse, tokenLoginData, editUser
from app.domain.model.user import User
from app.repository.userRepo import UserRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from app.utils.security.hash import hash_password, verify_password
from app.utils.security.jwt_handler import verify_access_token

#initalize the user service
class UserService:
    def __init__(self, db):
        # print("UserService")
        self.user_repo = UserRepository(db)
    
    #get all users
    def get_all_users(self):
        print("get_all_users")
        users = self.user_repo.get_all_users()
        #convert the users to response model
        
        users_response = [UserResponse.model_validate(user) for user in users]
        #return the response
        response = {"detail": "Users retrieved successfully", "data": users_response}
        return response

    #get user by id
    def get_user_by_id(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        #check if user exists
        if not user:
            raise NotFoundError(detail="User with this id does not exist")
        #convert the user to response model
        user_response = UserResponse.model_validate(user)

        # user_response = UserResponse(
        #     id=user.id,
        #     username=user.username,
        #     full_name=user.full_name,
        #     email=user.email,
        #     phone_number=user.phone_number,
        #     role=user.role,
        #     is_active=user.is_active
        # )
        #return the response
        response = {"detail": "User retrieved successfully", "data": user_response}
        return response
    
    #deactivate user
    def deactivate_user(self, user_id: int):
        user = self.user_repo.deactivate_user(user_id)
        #check if user exists
        if not user:
            raise NotFoundError(detail="User with this id does not exist")
        #convert the user to response model
        user_response = UserResponse.model_validate(user)

        # user_response = UserResponse(
        #     id=user.id,
        #     username=user.username,
        #     full_name=user.full_name,
        #     email=user.email,
        #     phone_number=user.phone_number,
        #     role=user.role,
        #     is_active=user.is_active
        # )
        #return the response
        response = {"detail": "User deactivated successfully", "data": user_response}
        return response
        
    #activate user
    def activate_user(self, user_id: int):
        user = self.user_repo.activate_user(user_id)
        #check if user exists
        if not user:
            raise NotFoundError(detail="User with this id does not exist")
        #convert the user to response model
        user_response = UserResponse.model_validate(user)

        # user_response = UserResponse(
        #     id=user.id,
        #     username=user.username,
        #     full_name=user.full_name,
        #     email=user.email,
        #     phone_number=user.phone_number,
        #     role=user.role,
        #     is_active=user.is_active
        # )
        #return the response
        response = {"detail": "User activated successfully", "data": user_response}
        return response
    
    #delete user
    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        
        try:
            self.user_repo.delete_user(user_id)
        except Exception as e:
            raise ValidationError(detail="An error occurred")
        
        response = {"detail": "User deleted successfully"}
        return response
    
    #update role
    def update_role(self, user_id: str, role: str):
        user = self.user_repo.update_role(user_id, role)
        #check if user exists
        if not user:
            raise NotFoundError(detail="User with this id does not exist")
        #convert the user to response model
        user_response = UserResponse.model_validate(user)

        # user_response = UserResponse(
        #     id=user.id,
        #     username=user.username,
        #     full_name=user.full_name,
        #     email=user.email,
        #     phone_number=user.phone_number,
        #     role=user.role,
        #     is_active=user.is_active
        # )
        #return the response
        response = {"detail": "User role updated successfully", "data": user_response}
        return response
    
    #get user by token
    def get_user_by_token(self, user_id):
        #split the token
        user = self.user_repo.get_user_by_id(user_id)
        #check if user exists
        if not user:
            raise NotFoundError(detail="User with this id does not exist")
        #convert the user to response model
        user_response = UserResponse.model_validate(user)
        # user_response = UserResponse(
        #     id=user.id,
        #     username=user.username,
        #     full_name=user.full_name,
        #     email=user.email,
        #     phone_number=user.phone_number,
        #     role=user.role,
        #     is_active=user.is_active
        # )
        #return the response
        response = {"detail": "User retrieved successfully", "data": user_response}
        return response
    
    #edit user by token
    def edit_user_by_token(self, user_id, edit_data: editUser):
        #split the token
        
        try:
            user = self.user_repo.update_user(user_id, edit_data)
        except IntegrityError as e:
            if "duplicate key" in str(e).lower():
                raise DuplicatedError(detail="User with this information already exists")
            raise ValidationError(detail="An error occurred with updating")
        #check if user exists
        if not user:
            raise NotFoundError(detail="User with this id does not exist")
        #convert the user to response model
        user_response = UserResponse.model_validate(user)
        
        # user_response = UserResponse(
        #     id=user.id,
        #     username=user.username,
        #     full_name=user.full_name,
        #     email=user.email,
        #     phone_number=user.phone_number,
        #     role=user.role,
        #     is_active=user.is_active
        # )
        #return the response
        response = {"detail": "User updated successfully", "data": user_response}
        return response

    #get all instructors
    def get_all_instructors(self):
        users = self.user_repo.get_all_instructors()
        users_response = [UserResponse.model_validate(user) for user in users]
        response = {"detail": "Instructors retrieved successfully", "data": users_response}
        return response

    #get instructor by id
    def get_instructor_by_id(self, instructor_id: str):
        user = self.user_repo.get_instructor_by_id(instructor_id)
        if not user:
            raise NotFoundError(detail="Instructor with this id does not exist")
        user_response = UserResponse.model_validate(user)
        response = {"detail": "Instructor retrieved successfully", "data": user_response}
        return response

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)