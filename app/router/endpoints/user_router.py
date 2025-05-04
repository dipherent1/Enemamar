from fastapi import APIRouter, Depends, status, HTTPException
from app.domain.schema.authSchema import editUser, UserResponse
from app.domain.schema.courseSchema import SearchParams
from app.service.userService import UserService, get_user_service
from app.utils.middleware.dependancies import is_logged_in
from uuid import UUID
from typing import Dict, Any, List

# User router for profile management
user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.get(
    "/me",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Retrieve the profile information of the currently authenticated user.",
    responses={
        200: {
            "description": "User profile retrieved successfully",
            "content": {
                "application/json": {
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
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Missing or invalid token"}
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
async def read_users_me(
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    """
    Retrieve the profile information of the currently authenticated user.

    This endpoint returns the complete profile of the user associated with the provided
    authentication token, including personal information and account details.

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)

    return user_service.get_user_by_token(user_id)

@user_router.put(
    "/me",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
    description="Update the profile information of the currently authenticated user.",
    responses={
        200: {
            "description": "User profile updated successfully",
            "content": {
                "application/json": {
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
        },
        400: {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email format"}
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Missing or invalid token"}
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        },
        409: {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "example": {"detail": "Username or email already exists"}
                }
            }
        }
    }
)
async def edit_me(
    edit_user: editUser,
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update the profile information of the currently authenticated user.

    This endpoint allows users to update their profile information such as username,
    email, first name, last name, and phone number.

    - **edit_user**: Object containing the fields to update (all fields are optional)

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)

    return user_service.edit_user_by_token(user_id, edit_user)

@user_router.delete("/me")
async def delete_me(
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    """
    Deactivate the current user's account.

    Args:
        decoded_token (dict): The decoded JWT token.
        user_service (UserService): The user service.

    Returns:
        dict: The deactivation response.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return user_service.deactivate_user(user_id)

# @user_router.get("/all")
# async def get_all_users(
#     params: SearchParams = Depends(),
#     user_service: UserService = Depends(get_user_service)
# ):
#     """
#     Get all users.

#     Args:
#         params (SearchParams): The search parameters.
#         user_service (UserService): The user service.

#     Returns:
#         dict: The users response.
#     """
#     return user_service.get_all_users(
#         search=params.search,
#         page=params.page,
#         page_size=params.page_size,
#         filter=params.filter
#     )

@user_router.get("/{user_id}")
async def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Get a user by ID.

    Args:
        user_id (str): The user ID.
        user_service (UserService): The user service.

    Returns:
        dict: The user profile.
    """
    return user_service.get_user_by_id(user_id)

# Instructor router
instructor_router = APIRouter(
    prefix="/instructors",
    tags=["instructor"]
)

@instructor_router.get("/")
async def get_all_instructors(
    params: SearchParams = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get all instructors.

    Args:
        params (SearchParams): The search parameters.
        user_service (UserService): The user service.

    Returns:
        dict: The instructors response.
    """
    return user_service.get_all_instructors(
        search=params.search,
        page=params.page,
        page_size=params.page_size
    )

@instructor_router.get("/{instructor_id}")
async def get_instructor_by_id(
    instructor_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Get an instructor by ID.

    Args:
        instructor_id (str): The instructor ID.
        user_service (UserService): The user service.

    Returns:
        dict: The instructor profile.
    """
    return user_service.get_instructor_by_id(instructor_id)
