from fastapi import APIRouter, Depends
from app.domain.schema.courseSchema import (
    SearchParams,
)
from app.service.courseService import CourseService, get_course_service
from app.utils.middleware.dependancies import is_logged_in
from uuid import UUID

# Course router
course_router = APIRouter(
    prefix="/courses",
    tags=["course"]
)

@course_router.get("/")
async def get_courses(
    search_params: SearchParams = Depends(),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get all courses.
    
    Args:
        search_params (SearchParams): The search parameters.
        course_service (CourseService): The course service.
        
    Returns:
        dict: The courses response.
    """
    return course_service.getCourses(
        page=search_params.page,
        page_size=search_params.page_size,
        search=search_params.search,
        filter=search_params.filter
    )

@course_router.get("/enrolled")
async def get_enrolled_courses(
    search_params: SearchParams = Depends(),
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get all courses enrolled by the current user.
    
    Args:
        search_params (SearchParams): The search parameters.
        decoded_token (dict): The decoded JWT token.
        course_service (CourseService): The course service.
        
    Returns:
        dict: The enrolled courses response.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    response = course_service.getEnrolledCourses(
        user_id=user_id,
        page=search_params.page,
        page_size=search_params.page_size,
        search=search_params.search
    )
    return response

@course_router.get("/{course_id}")
async def get_course(
    course_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get a course by ID.
    
    Args:
        course_id (str): The course ID.
        course_service (CourseService): The course service.
        
    Returns:
        dict: The course response.
    """
    course_response = course_service.getCourse(course_id)
    return course_response

# Analysis router
analysis_router = APIRouter(
    prefix="/analysis",
    tags=["course"]
)

@analysis_router.get("/instructor/{instructor_id}")
async def get_courses_by_instructor(
    instructor_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get courses by instructor.
    
    Args:
        instructor_id (str): The instructor ID.
        course_service (CourseService): The course service.
        
    Returns:
        dict: The courses response.
    """
    return course_service.get_intructor_course(
        instructor_id,
    )

@analysis_router.get("/{course_id}")
async def get_courses_analysis(
    course_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get course analysis.
    
    Args:
        course_id (str): The course ID.
        course_service (CourseService): The course service.
        
    Returns:
        dict: The course analysis response.
    """
    return course_service.get_courses_analysis(course_id)
