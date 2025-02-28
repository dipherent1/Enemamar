from fastapi import FastAPI
from app.router.routers import routers
from app.core.config.database import Base, engine


print("initializing app")
class AppCreator():
    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(routers)

Base.metadata.drop_all(bind=engine) 
Base.metadata.create_all(bind=engine)

app = AppCreator().app