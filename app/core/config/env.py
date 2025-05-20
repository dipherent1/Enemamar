from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SENTRY_DNS: str
    BASE_URL: str

    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ENCRIPTION_SECRET_KEY: str
    
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int  
    SMS_TOKEN: str
    SMS_ID: str
    CHAPA_PUBLIC_KEY: str
    CHAPA_SECRET_KEY: str   
    CHAPA_ENCRIPTION_KEY: str

    BUNNY_CDN_PULL_ZONE: str
    BUNNY_CDN_THUMB_STORAGE_ZONE: str
    BUNNY_CDN_THUMB_STORAGE_APIKEY: str
    BUNNY_CDN_PROFILE_STORAGE_ZONE: str
    BUNNY_CDN_PROFILE_STORAGE_APIKEY: str

    

    class Config:
        env_file = ".env"  # Specify the .env file to load variables from


def get_settings():
    return Settings()
