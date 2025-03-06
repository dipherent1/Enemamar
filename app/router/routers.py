from fastapi import APIRouter
from app.router.endpoints.authRouter import authRouter
from app.router.endpoints.userRouter import userRouter, rootRouter, instructorRouter
from app.router.endpoints.courseRouter import courseRouter, protected_courseRouter

routers = APIRouter()

routerList = [authRouter, userRouter, rootRouter, courseRouter, instructorRouter, protected_courseRouter]

for router in routerList:
    routers.include_router(router)