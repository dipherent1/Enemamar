from fastapi import APIRouter
from app.router.endpoints.authRouter import authRouter
from app.router.endpoints.userRouter import userRouter, rootRouter, instructorRouter
from app.router.endpoints.courseRouter import courseRouter

routers = APIRouter()

routerList = [authRouter, userRouter, rootRouter, courseRouter, instructorRouter]

for router in routerList:
    routers.include_router(router)