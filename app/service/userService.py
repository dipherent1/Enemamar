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
from typing import Optional

#initalize the user service
class UserService:
    def __init__(self, db):
        # print("UserService")
        self.user_repo = UserRepository(db)

    #get all users
    def get_all_users(self, search: Optional[str] = None, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        # Ensure pagination defaults when parameters are None
        page = page or 1
        page_size = page_size or 10
        users, err = self.user_repo.get_all_users(search=search, page=page, page_size=page_size, filter=filter)
        if err:
            raise ValidationError(detail="Failed to retrieve users", data=str(err))
        users_response = [UserResponse.model_validate(user) for user in users]
        response = {
            "detail": "Users retrieved successfully",
            "data": users_response,
            "page": page,
            "page_size": page_size
        }
        return response

    #get user by id
    def get_user_by_id(self, user_id: int):
        user, err = self.user_repo.get_user_by_id(user_id)
        if err:
            if isinstance(err, NotFoundError):
                raise NotFoundError(detail="User with this id does not exist")
            raise ValidationError(detail="Failed to retrieve user", data=str(err))
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
        user, err = self.user_repo.deactivate_user(user_id)
        if err:
            if isinstance(err, NotFoundError):
                raise NotFoundError(detail="User with this id does not exist")
            raise ValidationError(detail="Failed to deactivate user", data=str(err))
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
        user, err = self.user_repo.activate_user(user_id)
        if err:
            if isinstance(err, NotFoundError):
                raise NotFoundError(detail="User with this id does not exist")
            raise ValidationError(detail="Failed to activate user", data=str(err))
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
        # First check if user exists
        self.get_user_by_id(user_id)

        _, err = self.user_repo.delete_user(user_id)
        if err:
            raise ValidationError(detail="Failed to delete user", data=str(err))

        response = {"detail": "User deleted successfully"}
        return response

    #update role
    def update_role(self, user_id: str, role: str):
        user, err = self.user_repo.update_role(user_id, role)
        if err:
            if isinstance(err, NotFoundError):
                raise NotFoundError(detail="User with this id does not exist")
            raise ValidationError(detail="Failed to update user role", data=str(err))
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
        user, err = self.user_repo.get_user_by_id(user_id)
        if err:
            if isinstance(err, NotFoundError):
                raise NotFoundError(detail="User with this id does not exist")
            raise ValidationError(detail="Failed to retrieve user", data=str(err))
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

        user, err = self.user_repo.update_user(user_id, edit_data)
        if err:
            if isinstance(err, IntegrityError) and "duplicate key" in str(err).lower():
                raise DuplicatedError(detail="User with this information already exists")
            if isinstance(err, NotFoundError):
                raise NotFoundError(detail="User with this id does not exist")
            raise ValidationError(detail="Failed to update user", data=str(err))
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
    def get_all_instructors(self, search: Optional[str] = None, page: int = 1, page_size: int = 10):
        # Ensure pagination defaults when parameters are None
        page = page or 1
        page_size = page_size or 10
        users, err = self.user_repo.get_all_instructors(search=search, page=page, page_size=page_size)
        if err:
            raise ValidationError(detail="Failed to retrieve instructors", data=str(err))
        users_response = [UserResponse.model_validate(user) for user in users]
        response = {
            "detail": "Instructors retrieved successfully",
            "data": users_response,
            "page": page,
            "page_size": page_size
        }
        return response

    #get instructor by id
    def get_instructor_by_id(self, instructor_id: str):
        user, err = self.user_repo.get_instructor_by_id(instructor_id)
        if err:
            if isinstance(err, NotFoundError):
                raise NotFoundError(detail="Instructor with this id does not exist")
            raise ValidationError(detail="Failed to retrieve instructor", data=str(err))
        if not user:
            raise NotFoundError(detail="Instructor with this id does not exist")
        user_response = UserResponse.model_validate(user)
        response = {"detail": "Instructor retrieved successfully", "data": user_response}
        return response

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)