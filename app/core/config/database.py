from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config.env import get_settings





settings = get_settings()
DATABASE_URL = f"postgresql://{settings.USERNAME}:{settings.PASSWORD}@{settings.HOST}/{settings.DATABASE}"


# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
        print("----database initialized")
        
    finally:
        db.close()