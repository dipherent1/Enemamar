from fastapi import APIRouter, HTTPException, Request
from app.domain.schema.authSchema import signUp,login
from app.service.authService import AuthService
from fastapi import Depends, Header
from app.service.authService import get_auth_service
from app.utils.middleware.dependancies import is_admin, is_logged_in


authRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)



@authRouter.post("/signup")
async def signup(sign_up_info: signUp, auth_service: AuthService = Depends(get_auth_service)):
    userResponse = auth_service.signUp(sign_up_info)
    return userResponse

#login
@authRouter.post("/login")
async def login_endpoint(
    login_info: login,
    auth_service: AuthService = Depends(get_auth_service)
):
    # Validate input before processing
    print("login_info",login_info)
    try:
        login_info.validate()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return auth_service.login(login_info)

@authRouter.get("/refresh")
async def refresh_token(
    #get access token
    decoded_token: dict = Depends(is_logged_in),
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.refresh_token(decoded_token)
    