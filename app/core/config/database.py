from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config.env import get_settings, clear_settings_cache

# Clear the settings cache to ensure we get fresh settings
clear_settings_cache()

settings = get_settings()
DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DATABASE}"

# Create the SQLAlchemy engine
try:
    engine = create_engine(DATABASE_URL)
    print(f"----database url: {DATABASE_URL}")
except Exception as e:
    print(f"----database connection failed: {e}")
    raise

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
