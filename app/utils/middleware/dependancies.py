from fastapi import Depends, HTTPException, Header
from app.utils.security.jwt_handler import verify_access_token

def is_admin(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing access token")

    # ✅ Decode the token to get user details
    token = authorization.split("Bearer ")[1]
    decoded_token = verify_access_token(token)

    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid access token")

    # ✅ Check if the user has admin privileges
    if decoded_token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can access this resource")

    return decoded_token  # ✅ Return the decoded user data if admin

#is logged in 
def is_logged_in(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing access token")
    
    # ✅ Decode the token to get user details
    token = authorization.split("Bearer ")[1]
    decoded_token = verify_access_token(token)

    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    return decoded_token  # ✅ Return the decoded user data if logged in

    