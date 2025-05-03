from fastapi import APIRouter, Depends
from app.domain.schema.authSchema import editUser
from app.domain.schema.courseSchema import SearchParams
from app.service.userService import UserService, get_user_service
from app.utils.middleware.dependancies import is_logged_in
from uuid import UUID

# User router for profile management
user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.get("/me")
async def read_users_me(
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get the current user's profile.
    
    Args:
        decoded_token (dict): The decoded JWT token.
        user_service (UserService): The user service.
        
    Returns:
        dict: The user profile.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    
    return user_service.get_user_by_token(user_id)

@user_router.put("/me")
async def edit_me(
    edit_user: editUser, 
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update the current user's profile.
    
    Args:
        edit_user (editUser): The user update information.
        decoded_token (dict): The decoded JWT token.
        user_service (UserService): The user service.
        
    Returns:
        dict: The updated user profile.
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
