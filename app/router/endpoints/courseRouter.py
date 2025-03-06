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
    ModuleResponse,
    LessonInput,
    LessonResponse,
    MultipleLessonInput
)
from app.service.courseService import CourseService
from fastapi import Depends, Header
from app.service.courseService import get_course_service
from app.utils.middleware.dependancies import is_admin, is_logged_in
from uuid import UUID
from typing import Union, List

courseRouter = APIRouter(
    prefix="/course",
    tags=["course"]
)


#get all courses enrolled by user
@courseRouter.get("/enrolled")
async def get_enrolled_courses(
    search_params: CourseSearchParams = Depends(),
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    enrollments = course_service.getEnrolledCourses(
        user_id=user_id,
        page=search_params.page,
        page_size=search_params.page_size,
        search=search_params.search
    )
    return enrollments

#add multiple lessons to course
@courseRouter.post("/{course_id}/lessons")
async def add_multiple_lessons(
    course_id: str,
    lessons_input: MultipleLessonInput,  # Change the parameter name to be more clear
    course_service: CourseService = Depends(get_course_service)
):
    return course_service.addMultipleLessons(course_id, lessons_input)

#get all lessons of course
@courseRouter.get("/{course_id}/lessons")
async def get_lessons(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    search_params: PaginationParams = Depends(),
    course_service: CourseService = Depends(get_course_service)
):
    user_id = decoded_token.get("id")
    return course_service.getLessons(
        course_id,
        user_id,
        search_params.page,
        search_params.page_size
    )

#get lesson by id
@courseRouter.get("/{course_id}/lesson/{lesson_id}")
async def get_lesson_by_id(
    course_id: str,
    lesson_id: str,
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    user_id = decoded_token.get("id")
    return course_service.getLessonById(course_id, lesson_id, user_id)

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

#create protected router for admin
protected_courseRouter = APIRouter(
    prefix="protected/course",
    tags=["course"],
    dependencies=[Depends(is_admin)]
)

#add course 
@protected_courseRouter.post("/add")
async def add_course(
    course_info: CourseInput,
    course_service: CourseService = Depends(get_course_service),
    # _: dict = Depends(is_admin)  # Only admins can create courses
):
    return course_service.addCourse(course_info)