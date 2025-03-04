from fastapi import APIRouter, HTTPException, Request
from app.domain.schema.courseSchema import (
    CourseInput,
    CourseResponse,
    CreateCourseResponse,
    EnrollmentResponse,
    EnrollResponse,
    PaginationParams,
    CourseSearchParams,
    ModuleInput,
    ModuleResponse
)
from app.service.courseService import CourseService
from fastapi import Depends, Header
from app.service.courseService import get_course_service
from app.utils.middleware.dependancies import is_admin, is_logged_in
from uuid import UUID
courseRouter = APIRouter(
    prefix="/course",
    tags=["course"]
)

#add course 
@courseRouter.post("/add")
async def add_course(
    course_info: CourseInput,
    course_service: CourseService = Depends(get_course_service)
):
    courseResponse = course_service.addCourse(course_info)
    return courseResponse

#get all courses enrolled by user
@courseRouter.get("/enrolled")
async def get_courses_by_user(
    search_params: CourseSearchParams = Depends(),
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    enrollments = course_service.getCoursesByUser(
        user_id=user_id,
        page=search_params.page,
        page_size=search_params.page_size,
        search=search_params.search
    )
    return enrollments

#add module to course
@courseRouter.post("/{course_id}/module")
async def add_module(
    course_id: str,
    module_info: ModuleInput,
    course_service: CourseService = Depends(get_course_service)
):
    moduleResponse = course_service.addModule(course_id, module_info)
    return moduleResponse

#get all modules of course
@courseRouter.get("/{course_id}/modules")
async def get_modules(
    course_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    modules = course_service.getModules(course_id)
    return modules

#get module by using module id
@courseRouter.get("/{course_id}/module/{module_id}")
async def get_module(
    course_id: str,
    module_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    module = course_service.getModule(course_id, module_id)
    return module

#get course by using course id
@courseRouter.get("/{course_id}")
async def get_course(
    course_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    courseResponse = course_service.getCourse(course_id)
    return courseResponse

#get all courses
@courseRouter.get("/")
async def get_courses(
    search_params: CourseSearchParams = Depends(),
    course_service: CourseService = Depends(get_course_service)
):
    return course_service.getCourses(
        page=search_params.page,
        page_size=search_params.page_size,
        search=search_params.search
    )

#enroll course only for logged in user
@courseRouter.post("/{course_id}/enroll")
async def enroll_course(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    user_id = decoded_token.get("id")
   
    user_id = UUID(user_id)
    course_id = UUID(course_id)
   
    enrollResponse = course_service.enrollCourse(user_id, course_id)
    return enrollResponse
