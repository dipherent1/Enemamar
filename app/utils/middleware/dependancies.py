from fastapi import Depends, HTTPException, Header, Request
from app.utils.security.jwt_handler import verify_access_token
from typing import Optional

async def is_admin(request: Request):
    """Middleware-like dependency to check authentication via JWT token."""
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    # ✅ Decode the token to get user details
    token = token.split("Bearer ")[1]
    decoded_token = verify_access_token(token)

    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid access token")

    # ✅ Check if the user has admin privileges
    if decoded_token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can access this resource")

    return decoded_token  # ✅ Return the decoded user data if admin

#is logged in 
async def is_logged_in(request: Request):
    """Middleware-like dependency to check authentication via JWT token."""
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = token.split(" ")[1]  # Extract token after "Bearer"
    user_data = verify_access_token(token)

    return user_data # Return decoded user info

