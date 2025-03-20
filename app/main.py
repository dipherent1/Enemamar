from fastapi import FastAPI
from app.router.routers import routers
from app.core.config.database import Base, engine
from sqlalchemy import text


print("initializing app")
class AppCreator():
    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(routers)

# Drop all tables with CASCADE
with engine.connect() as connection:
    # Disable foreign key checks temporarily
    connection.execute(text("DROP SCHEMA public CASCADE;"))
    connection.execute(text("CREATE SCHEMA public;"))
    connection.execute(text('GRANT ALL ON SCHEMA public TO postgres;'))
    connection.execute(text('GRANT ALL ON SCHEMA public TO public;'))
    connection.commit()

# Recreate all tables
Base.metadata.create_all(bind=engine)

app = AppCreator().app