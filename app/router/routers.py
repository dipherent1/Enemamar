from fastapi import APIRouter
from app.router.endpoints.auth_router import auth_router
from app.router.endpoints.admin_router import admin_router, inst_admin_router
from app.router.endpoints.user_router import user_router, instructor_router
from app.router.endpoints.course_router import course_router, analysis_router
from app.router.endpoints.payment_router import payment_router, protected_payment_router
from app.router.endpoints.lesson_router import lesson_router, protected_lesson_router

routers = APIRouter()

routerList = [
    # Auth endpoints
    auth_router,

    # User endpoints
    user_router,
    instructor_router,

    # Course endpoints
    course_router,
    analysis_router,

    # Lesson endpoints
    lesson_router,
    protected_lesson_router,

    # Payment endpoints
    payment_router,
    protected_payment_router,

    # Admin endpoints
    admin_router,
    inst_admin_router,
]

for router in routerList:
    routers.include_router(router)