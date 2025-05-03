from fastapi import APIRouter, HTTPException, Request, Depends, Header
from app.domain.schema.authSchema import signUp, login, RefreshTokenRequest
from app.service.authService import AuthService, get_auth_service
from app.utils.middleware.dependancies import is_admin, is_logged_in

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/otp/send")
async def send_otp(phone_number: str, auth_service: AuthService = Depends(get_auth_service)):
    """
    Send OTP to the provided phone number.
    
    Args:
        phone_number (str): The phone number to send OTP to.
        auth_service (AuthService): The authentication service.
        
    Returns:
        dict: The OTP response.
    """
    return auth_service.send_otp(phone_number=phone_number)

@auth_router.post("/otp/verify")
async def verify_otp(phone_number: str, code: str, auth_service: AuthService = Depends(get_auth_service)):
    """
    Verify OTP for the provided phone number.
    
    Args:
        phone_number (str): The phone number to verify OTP for.
        code (str): The OTP code.
        auth_service (AuthService): The authentication service.
        
    Returns:
        dict: The verification response.
    """
    return auth_service.verify_otp(phone_number=phone_number, code=code)

@auth_router.post("/signup")
async def signup(sign_up_info: signUp, auth_service: AuthService = Depends(get_auth_service)):
    """
    Register a new user.
    
    Args:
        sign_up_info (signUp): The user registration information.
        auth_service (AuthService): The authentication service.
        
    Returns:
        dict: The registration response.
    """
    user_response = auth_service.signUp(sign_up_info)
    return user_response

@auth_router.post("/login")
async def login_endpoint(
    login_info: login,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate a user.
    
    Args:
        login_info (login): The login information.
        auth_service (AuthService): The authentication service.
        
    Returns:
        dict: The login response.
    """
    try:
        login_info.validate()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return auth_service.login(login_info)

@auth_router.post("/logout")
async def logout(refresh_token: str = Header(None), auth_service: AuthService = Depends(get_auth_service)):
    """
    Log out a user.
    
    Args:
        refresh_token (str): The refresh token.
        auth_service (AuthService): The authentication service.
        
    Returns:
        dict: The logout response.
    """
    return auth_service.logout(refresh_token=refresh_token)

@auth_router.post("/refresh")
async def refresh_token(
    refresh_token_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Refresh an access token.
    
    Args:
        refresh_token_request (RefreshTokenRequest): The refresh token request.
        auth_service (AuthService): The authentication service.
        
    Returns:
        dict: The token refresh response.
    """
    return auth_service.refresh_token(refresh_token=refresh_token_request.refresh_token)
