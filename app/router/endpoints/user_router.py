from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from app.domain.schema.authSchema import editUser, UserResponse
from app.domain.schema.courseSchema import SearchParams
from app.domain.schema.responseSchema import (
    UserProfileResponse, UserUpdateResponse, BaseResponse,
    ErrorResponse, PaginatedResponse
)
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
    # response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Retrieve the profile information of the currently authenticated user.",
    # responses={
    #     200: {
    #         "description": "User profile retrieved successfully",
    #         "model": UserProfileResponse
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "User not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "User not found"}
    #             }
    #         }
    #     }
    # }
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
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
    description="Update the profile information of the currently authenticated user.",
    # responses={
    #     200: {
    #         "description": "User profile updated successfully",
    #         "model": UserUpdateResponse
    #     },
    #     400: {
    #         "description": "Bad request",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Invalid email format"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "User not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "User not found"}
    #             }
    #         }
    #     },
    #     409: {
    #         "description": "Conflict",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Username or email already exists"}
    #             }
    #         }
    #     }
    # }
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

@user_router.delete(
    "/me",
    # response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate user account",
    description="Deactivate the current user's account.",
    # responses={
    #     200: {
    #         "description": "Account deactivated successfully",
    #         "model": BaseResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Account deactivated successfully"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "User not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "User not found"}
    #             }
    #         }
    #     }
    # }
)
async def delete_me(
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    """
    Deactivate the current user's account.

    This endpoint marks the user account as inactive, effectively deactivating it.
    The account data is preserved but the user will no longer be able to log in.

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return user_service.deactivate_user(user_id)

@user_router.post(
    "/me/profile-picture",
    status_code=status.HTTP_200_OK,
    summary="Upload profile picture",
    description="Upload a profile picture for the current user."
)
async def upload_profile_picture(
    profile_picture: UploadFile = File(...),
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    """
    Upload a profile picture for the current user.

    This endpoint allows users to upload a profile picture. The image will be stored
    in BunnyCDN and the URL will be saved in the user's profile.

    - **profile_picture**: The image file to upload (JPEG or PNG)

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)

    return user_service.upload_profile_picture(str(user_id), profile_picture)

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

@user_router.get(
    "/{user_id}",
    # response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Retrieve a user's profile by their ID.",
    # responses={
    #     200: {
    #         "description": "User profile retrieved successfully",
    #         "model": UserProfileResponse
    #     },
    #     404: {
    #         "description": "User not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "User not found"}
    #             }
    #         }
    #     }
    # }
)
async def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Retrieve a user's profile by their ID.

    This endpoint returns the public profile information of a user identified by their UUID.

    - **user_id**: UUID of the user to retrieve
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
    Get all instructors with search capabilities.

    This endpoint returns a paginated list of all users with instructor role.
    You can search across multiple instructor fields.

    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    - **search**: Optional search term to filter instructors by username, email, phone number, first name, last name, or profession

    Args:
        params (SearchParams): The search parameters.
        user_service (UserService): The user service.

    Returns:
        dict: The instructors response with pagination metadata.
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
