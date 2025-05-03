from fastapi import Depends, HTTPException, Header, Request
from app.utils.security.jwt_handler import verify_access_token
from typing import Optional

async def is_logged_in(request: Request):
    """Middleware-like dependency to check authentication via JWT token."""
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = token.split(" ")[1]  # Extract token after "Bearer"
    user_data = verify_access_token(token)

    return user_data # Return decoded user info

async def is_admin(request: Request):
    decoded_token = await is_logged_in(request)

    # ✅ Check if the user has admin privileges
    if decoded_token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can access this resource")

    return decoded_token  # ✅ Return the decoded user data if admin

#is admin or instructor
async def is_admin_or_instructor(request: Request):
    decoded_token = await is_logged_in(request)

    # ✅ Check if the user has admin or instructor privileges
    if decoded_token.get("role") not in ["admin", "instructor"]:
        raise HTTPException(status_code=403, detail="Only admins or instructors can access this resource")

    return decoded_token  # ✅ Return the decoded user data if admin or instructor
#is logged in 

