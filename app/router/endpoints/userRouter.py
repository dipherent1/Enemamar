from fastapi import APIRouter, HTTPException, Request
from app.domain.schema.authSchema import signUp,login,editUser, UpdateRoleRequest
from app.domain.schema.courseSchema import SearchParams
from fastapi import Depends, Header
from app.service.userService import UserService, get_user_service
from app.utils.middleware.dependancies import is_admin, is_logged_in
from uuid import UUID
from typing import Optional


userRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(is_admin)]
)


#deactivate user
@userRouter.put("/deactivate/{user_id}")
async def deactivate_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    return user_service.deactivate_user(user_id)

#activate user
@userRouter.put("/activate/{user_id}")
async def activate_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    return user_service.activate_user(user_id)

#delete user
@userRouter.delete("/{user_id}")
async def delete_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    return user_service.delete_user(user_id)



@userRouter.put("/role/{user_id}")
async def update_role(
    user_id: str, 
    role_data: UpdateRoleRequest, 
    user_service: UserService = Depends(get_user_service)
):
    return user_service.update_role(user_id, role_data.role)


#user profile router
rootRouter = APIRouter()

@rootRouter.get("/me")
async def read_users_me(
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    print("/me")
    
    return user_service.get_user_by_token(user_id)

#edit me
@rootRouter.put("/me")
async def edit_me(
    edit_user: editUser, 
    decoded_token: dict = Depends(is_logged_in),
    user_service: UserService = Depends(get_user_service)
):
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    
    return user_service.edit_user_by_token(user_id,edit_user)

#delete


#get all users
@rootRouter.get("/all/users")
async def get_all_users(
    params: SearchParams = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_all_users(
        search=params.search,
        page=params.page,
        page_size=params.page_size,
        filter=params.filter
    )

#get user by id
@rootRouter.get("/user/{user_id}")
async def get_user_by_id(user_id: str, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_by_id(user_id)

#create router for instructor 
instructorRouter = APIRouter(
    prefix="/protected/users/instructors",
    tags=["instructor"],
)
#get all instructors
@instructorRouter.get("/")
async def get_all_instructors(
    params: SearchParams = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_all_instructors(
        search=params.search,
        page=params.page,
        page_size=params.page_size
    )

#get instructor by id
@instructorRouter.get("/{instructor_id}")
async def get_instructor_by_id(instructor_id: str, user_service: UserService = Depends(get_user_service)):
    print("get_instructor_by_id")
    return user_service.get_instructor_by_id(instructor_id)