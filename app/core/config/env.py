from dotenv import load_dotenv
import os
import sys

dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
else:
    load_dotenv()

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Print environment variables for debugging
    DATABASE: str = os.getenv("DATABASE")
    PORT: int = int(os.getenv("PORT", 0))
    DB_USERNAME: str = os.getenv("DB_USERNAME", os.getenv("USERNAME"))  # Try DB_USERNAME first, fall back to USERNAME
    PASSWORD: str = os.getenv("PASSWORD")
    HOST: str = os.getenv("HOST")

    ACCESS_SECRET_KEY: str = os.getenv("ACCESS_SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY")
    ENCRIPTION_SECRET_KEY: str = os.getenv("ENCRIPTION_SECRET_KEY")

    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 0))
    SMS_TOKEN: str = os.getenv("SMS_TOKEN")
    SMS_ID: str = os.getenv("SMS_ID")
    CHAPA_PUBLIC_KEY: str = os.getenv("CHAPA_PUBLIC_KEY")
    CHAPA_SECRET_KEY: str = os.getenv("CHAPA_SECRET_KEY")
    CHAPA_ENCRIPTION_KEY: str = os.getenv("CHAPA_ENCRIPTION_KEY")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Function to clear the settings cache if needed
def clear_settings_cache():
    get_settings.cache_clear()
