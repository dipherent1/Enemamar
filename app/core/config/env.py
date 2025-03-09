from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    HOST: str

    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ENCRIPTION_SECRET_KEY: str
    
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int  

    

    class Config:
        env_file = ".env"  # Specify the .env file to load variables from

# Cache the settings for efficient reuse
@lru_cache()
def get_settings():
    return Settings()
