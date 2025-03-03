from fastapi import APIRouter, HTTPException, Request
from app.domain.schema.courseSchema import CourseInput,CourseResponse,CreateCourseResponse,EnrollmentResponse,EnrollResponse
from app.service.courseService import CourseService
from fastapi import Depends, Header
from app.service.courseService import get_course_service
from app.utils.middleware.dependancies import is_admin

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