from fastapi import APIRouter, Depends, status
from app.domain.schema.courseSchema import (
    SearchParams,
    CourseResponse,
    EnrollmentResponse,
    EnrollResponse,
    CourseAnalysisResponse
)
from app.service.courseService import CourseService, get_course_service
from app.utils.middleware.dependancies import is_logged_in
from uuid import UUID
from typing import Dict, Any, List

# Course router
course_router = APIRouter(
    prefix="/courses",
    tags=["course"]
)

@course_router.get(
    "/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get all courses",
    description="Retrieve a paginated list of all available courses with optional filtering and search.",
    responses={
        200: {
            "description": "List of courses retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Courses retrieved successfully",
                        "data": {
                            "courses": [
                                {
                                    "id": "123e4567-e89b-12d3-a456-426614174000",
                                    "title": "Introduction to Python",
                                    "description": "Learn Python from scratch",
                                    "price": 99.99,
                                    "instructor_id": "123e4567-e89b-12d3-a456-426614174001"
                                }
                            ],
                            "total": 1,
                            "page": 1,
                            "page_size": 10,
                            "total_pages": 1
                        }
                    }
                }
            }
        },
        404: {
            "description": "No courses found",
            "content": {
                "application/json": {
                    "example": {"detail": "No courses found"}
                }
            }
        }
    }
)
async def get_courses(
    search_params: SearchParams = Depends(),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Retrieve a paginated list of all available courses.

    This endpoint returns a list of all courses in the system with pagination support.
    You can filter and search courses based on various criteria.

    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    - **search**: Optional search term to filter courses by title or description
    - **filter**: Optional filter parameter (e.g., 'price_low', 'price_high', 'newest')
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

@course_router.post("/enroll/{course_id}")
async def enroll_course(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Enroll in a course.

    Args:
        course_id (str): The course ID.
        decoded_token (dict): The decoded JWT token.
        course_service (CourseService): The course service.

    Returns:
        dict: The enrollment response.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return course_service.enrollCourse(
        user_id=user_id,
        course_id=course_id
    )
@course_router.delete("/enroll/{course_id}")
async def unenroll_course(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Unenroll from a course.

    Args:
        course_id (str): The course ID.
        decoded_token (dict): The decoded JWT token.
        course_service (CourseService): The course service.

    Returns:
        dict: The unenrollment response.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return course_service.unenrollCourse(
        user_id=user_id,
        course_id=course_id
    )

@course_router.get(
    "/{course_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get course by ID",
    description="Retrieve detailed information about a specific course by its ID.",
    responses={
        200: {
            "description": "Course retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Course retrieved successfully",
                        "data": {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Introduction to Python",
                            "description": "Learn Python from scratch",
                            "price": 99.99,
                            "discount": 0.1,
                            "thumbnail_url": "https://example.com/thumbnail.jpg",
                            "instructor_id": "123e4567-e89b-12d3-a456-426614174001",
                            "instructor": {
                                "id": "123e4567-e89b-12d3-a456-426614174001",
                                "first_name": "John",
                                "last_name": "Doe"
                            },
                            "lessons": [
                                {
                                    "id": "123e4567-e89b-12d3-a456-426614174002",
                                    "title": "Getting Started with Python",
                                    "description": "Learn the basics of Python programming",
                                    "duration": 30
                                }
                            ]
                        }
                    }
                }
            }
        },
        404: {
            "description": "Course not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Course not found"}
                }
            }
        }
    }
)
async def get_course(
    course_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Retrieve detailed information about a specific course.

    This endpoint returns comprehensive details about a course, including its lessons,
    instructor information, pricing, and other metadata.

    - **course_id**: UUID of the course to retrieve
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
