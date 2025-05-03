from fastapi import APIRouter
from app.router.endpoints.authRouter import authRouter
from app.router.endpoints.userRouter import userRouter, rootRouter, instructorRouter
from app.router.endpoints.courseRouter import courseRouter, protected_courseRouter, analysis_router
from app.router.endpoints.payment_router import payment_router, protected_payment_router
from app.router.endpoints.lesson_router import lesson_router, protected_lesson_router

routers = APIRouter()

routerList = [
    authRouter,
    userRouter,
    rootRouter,
    courseRouter,
    instructorRouter,
    protected_courseRouter,
    analysis_router,
    payment_router,
    protected_payment_router,
    lesson_router,
    protected_lesson_router
]

for router in routerList:
    routers.include_router(router)