from fastapi import APIRouter
from app.router.endpoints.authRouter import authRouter
from app.router.endpoints.userRouter import userRouter, rootRouter

routers = APIRouter()

routerList = [authRouter, userRouter, rootRouter]

for router in routerList:
    routers.include_router(router)