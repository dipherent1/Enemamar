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

@authRouter.post("/otp/send")
async def sendOTP(phone_number: str, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.send_otp(phone_number=phone_number)

@authRouter.post("/otp/verify")
async def verifyOTP(phone_number: str, code: str, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.verify_otp(phone_number=phone_number, code=code)



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

@authRouter.post("/logout")
async def logout(refresh_token: str = Header(None), auth_service:AuthService = Depends(get_auth_service)):

    return auth_service.logout(refresh_token=refresh_token)

@authRouter.get("/refresh")
async def refresh_token(
    #get access token
    refresh_token: str = Header(None),
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.refresh_token(refresh_token)
    