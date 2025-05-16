from app.utils.exceptions.exceptions import AuthError, NotFoundError,DuplicatedError,ValidationError
from sqlalchemy.orm import Session
from app.domain.model.user import User, RefreshToken
from app.domain.schema.authSchema import tokenLoginData, editUser
from app.utils.security.jwt_handler import create_access_token, create_refresh_token
from sqlalchemy.exc import DataError
from typing import Optional
from sqlalchemy import or_
from app.utils.security.hash import hash_password, verify_password

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            print("Error creating user:", e)
            return None

    def get_user_by_refresh(self, user_id: str, refresh_token: str):
        try:
            result = self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()
            if not result:
                return None

            if not verify_password(refresh_token,result.token):
                raise AuthError(detail="Invalid refresh token: token not verified")

            return result
        except Exception as e:
            print("Error getting user by refresh token:", e)
            return None

    def delete_refresh(self, user_id: str, refresh_token: str):
        try:
            refresh = self.get_user_by_refresh(user_id=user_id, refresh_token=refresh_token)
            if not refresh:
                return None

            self.db.delete(refresh)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print("Error deleting refresh token:", e)
            return None

    def get_all_users(self, search: Optional[str] = None, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        try:
            query = self.db.query(User).filter(User.is_active == True)
            if search:
                query = query.filter(
                    or_(
                        User.email.ilike(f"%{search}%"),
                        User.phone_number.ilike(f"%{search}%"),
                        User.first_name.ilike(f"%{search}%"),
                        User.last_name.ilike(f"%{search}%"),    
                        User.profession.ilike(f"%{search}%")
                    )
                )
            offset = (page - 1) * page_size
            return query.offset(offset).limit(page_size).all()
        except Exception as e:
            print("Error getting all users:", e)
            return None
    
    def get_user_by_id(self, user_id: str):
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except DataError as e:
            print("Error getting user by ID:", e)
            return None
    

    def get_user_by_email(self, email: str):
        try:
            return self.db.query(User).filter(User.email == email).first()
        except DataError as e:
            print("Error getting user by email:", e)
            return None

    def get_user_by_phone(self, phone_number: str):
        try:
            return self.db.query(User).filter(User.phone_number == phone_number).first()
        except DataError as e:
            print("Error getting user by phone:", e)
            return None

    def deactivate_user(self, user_id: int):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            user.is_active = False
            self.db.commit()
            return user
        except Exception as e:
            self.db.rollback()
            print("Error deactivating user:", e)
            return None

    def activate_user(self, user_id: Optional[str] = None, phone_number: Optional[str] = None):
        try:
            user = None
            if user_id:
                user = self.get_user_by_id(user_id)
            elif phone_number:
                print("from activate user", phone_number)
                user = self.get_user_by_phone(phone_number)
            
            if not user:
                return None
            
            user.is_active = True
            self.db.commit()
            print("User activated:", user.id)
            return user
        except Exception as e:
            self.db.rollback()
            print("Error activating user:", e)
            return None
    
    def delete_user(self, user_id: int):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User with this id does not exist")
            self.db.delete(user)
            self.db.commit()
            return
        except Exception as e:
            self.db.rollback()
            print("Error deleting user:", e)
            return None

    #update the role of the user
    def update_role(self, user_id: int, role: str):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            user.role = role
            self.db.commit()
            return user
        except Exception as e:
            self.db.rollback()
            print("Error updating user role:", e)
            return None

    def update_user(self,id:int, edit_user: editUser):
        try:
            user = self.db.query(User).filter(User.id == id).first()
            if not user:
                return None
            for key, value in edit_user.model_dump().items():
                if value:
                    setattr(user, key, value)
            self.db.commit()
            return user
        except Exception as e:
            self.db.rollback()
            print("Error updating user:", e)
            return None

    
    def login(self, login_data: tokenLoginData):
        try:
            accesToken = create_access_token(login_data.model_dump())
            refreshToken = create_refresh_token(login_data.model_dump())
            
            # check and delete if there is existing refresh token
            existing_refresh = self.get_refresh_token(login_data.id)
            if existing_refresh:
                self.db.delete(existing_refresh)
            
            # store hashed refresh token in database
            hashed_refresh_token = hash_password(refreshToken)
            self.db.add(RefreshToken(user_id=login_data.id, token=hashed_refresh_token))
            self.db.commit()
            
            return accesToken, refreshToken
        except Exception as e:
            print("Error during login:", e)
            self.db.rollback()
            return None, None

    def get_refresh_token(self, user_id: str):
        try:
            return self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()
        except Exception as e:
            print("Error getting refresh token:", e)
            return None

    def get_all_instructors(self, search: Optional[str] = None, page: int = 1, page_size: int = 10):
        try:
            query = self.db.query(User).filter(User.role == "instructor")
            
            if search:
                query = query.filter(
                    or_(
                        User.email.ilike(f"%{search}%"),
                        User.phone_number.ilike(f"%{search}%"),
                        User.first_name.ilike(f"%{search}%"),
                        User.last_name.ilike(f"%{search}%")
                    )
                )
            
            offset = (page - 1) * page_size
            return query.offset(offset).limit(page_size).all()
        except Exception as e:
            print("Error getting all instructors:", e)
            return None
    
    def get_instructor_by_id(self, instructor_id: str):
        try:
            return self.db.query(User).filter(User.id == instructor_id, User.role == "instructor").first()
        except DataError:
            return None
        except Exception as e:
            print("Error getting instructor by id:", e)
            return None
