from fastapi import APIRouter
from app.router.endpoints.authRouter import authRouter
from app.router.endpoints.userRouter import userRouter, rootRouter
from app.router.endpoints.applicationRouter import applicationRouter

routers = APIRouter()

routerList = [authRouter, userRouter, rootRouter, applicationRouter]

for router in routerList:
    routers.include_router(router)