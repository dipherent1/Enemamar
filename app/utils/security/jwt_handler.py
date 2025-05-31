from app.utils.exceptions.exceptions import HTTPException
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.core.config.env import get_settings
import uuid

settings = get_settings()

ACCESS_SECRET_KEY = settings.ACCESS_SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
PASSWORD_RESET_SECRET_KEY = settings.PASSWORD_RESET_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
ALGORITHM = "HS256"

def create_access_token(data: dict) -> str:
    """Generate a new access token."""
    to_encode = data.copy()
    # Convert UUID to string for JSON serialization
    for key, value in to_encode.items():
        if isinstance(value, uuid.UUID):
            to_encode[key] = str(value)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Generate a new refresh token."""
    to_encode = data.copy()
    for key, value in to_encode.items():
        if isinstance(value, uuid.UUID):
            to_encode[key] = str(value)
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> Optional[dict]:
    """Verify access token and return payload."""
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def verify_refresh_token(token: str) -> Optional[dict]:
    """Verify refresh token and return payload."""
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_password_reset_token(phone_number: str) -> str:
    """Generate a password reset token (expires in 10 minutes)."""
    to_encode = {
        "phone_number": phone_number,
        "type": "password_reset"
    }
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)  # 10 minute expiry
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, PASSWORD_RESET_SECRET_KEY, algorithm=ALGORITHM)


def verify_password_reset_token(token: str) -> Optional[dict]:
    """Verify password reset token and return payload."""
    try:
        payload = jwt.decode(token, PASSWORD_RESET_SECRET_KEY, algorithms=[ALGORITHM])

        # Verify it's a password reset token
        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=401, detail="Invalid token type")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Password reset token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid password reset token")

