import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.core.config.env import get_settings
import uuid

settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def verify_refresh_token(token: str) -> Optional[dict]:
    """Verify refresh token and return payload."""
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
