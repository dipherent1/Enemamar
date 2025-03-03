from fastapi import APIRouter, HTTPException, Request
from app.domain.schema.courseSchema import CourseInput,CourseResponse,CreateCourseResponse,EnrollmentResponse,EnrollResponse, PaginationParams
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
    pagination: PaginationParams = Depends(),
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    enrollments = course_service.getCoursesByUser(
        user_id=user_id,
        page=pagination.page,
        page_size=pagination.page_size
    )
    return enrollments

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
    pagination: PaginationParams = Depends(),
    course_service: CourseService = Depends(get_course_service)
):
    return course_service.getCourses(
        page=pagination.page,
        page_size=pagination.page_size
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
