from fastapi import APIRouter, Depends, status
from app.domain.schema.courseSchema import (
    SearchParams,
    CourseResponse,
    EnrollmentResponse,
    EnrollResponse,
    CourseAnalysisResponse
)
from app.domain.schema.responseSchema import (
    CourseListResponse, CourseDetailResponse, EnrollmentResponse as EnrollmentResponseModel,
    BaseResponse, ErrorResponse, PaginatedResponse
)
from app.service.courseService import CourseService, get_course_service
from app.utils.middleware.dependancies import is_logged_in
from uuid import UUID
from typing import Dict, Any

# Course router
course_router = APIRouter(
    prefix="/courses",
    tags=["course"]
)

@course_router.get(
    "/",
    # response_model=CourseListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all courses",
    description="Retrieve a paginated list of all available courses with optional filtering and search.",
    # responses={
    #     200: {
    #         "description": "List of courses retrieved successfully",
    #         "model": CourseListResponse
    #     },
    #     404: {
    #         "description": "No courses found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "No courses found"}
    #             }
    #         }
    #     }
    # }
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

@course_router.get(
    "/enrolled",
    # response_model=CourseListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get enrolled courses",
    description="Retrieve a paginated list of courses enrolled by the current user.",
    # responses={
    #     200: {
    #         "description": "Enrolled courses retrieved successfully",
    #         "model": CourseListResponse
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "No enrolled courses found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "No enrolled courses found"}
    #             }
    #         }
    #     }
    # }
)
async def get_enrolled_courses(
    search_params: SearchParams = Depends(),
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Retrieve a paginated list of courses enrolled by the current user.

    This endpoint returns all courses that the authenticated user has enrolled in,
    with pagination support and optional search functionality.

    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    - **search**: Optional search term to filter enrolled courses by title or description

    Authentication is required via JWT token in the Authorization header.
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

@course_router.post(
    "/enroll/{course_id}",
    # response_model=EnrollmentResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Enroll in a course",
    description="Enroll the current user in a specific course.",
    # responses={
    #     201: {
    #         "description": "Successfully enrolled in course",
    #         "model": EnrollmentResponseModel
    #     },
    #     400: {
    #         "description": "Bad request",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Already enrolled in this course"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def enroll_course(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Enroll the current user in a specific course.

    This endpoint creates an enrollment record linking the authenticated user to the specified course.
    If the course requires payment, this endpoint will initiate the payment process.

    - **course_id**: UUID of the course to enroll in

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return course_service.enrollCourse(
        user_id=user_id,
        course_id=course_id
    )
@course_router.delete(
    "/enroll/{course_id}",
    # response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Unenroll from a course",
    description="Unenroll the current user from a specific course.",
    # responses={
    #     200: {
    #         "description": "Successfully unenrolled from course",
    #         "model": BaseResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Successfully unenrolled from course"}
    #             }
    #         }
    #     },
    #     400: {
    #         "description": "Bad request",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Not enrolled in this course"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def unenroll_course(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Unenroll the current user from a specific course.

    This endpoint removes the enrollment record linking the authenticated user to the specified course.

    - **course_id**: UUID of the course to unenroll from

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return course_service.unenrollCourse(
        user_id=user_id,
        course_id=course_id
    )

@course_router.get(
    "/{course_id}",
    # response_model=CourseDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get course by ID",
    description="Retrieve detailed information about a specific course by its ID.",
    # responses={
    #     200: {
    #         "description": "Course retrieved successfully",
    #         "model": CourseDetailResponse
    #     },
    #     404: {
    #         "description": "Course not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
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

@analysis_router.get(
    "/instructor/{instructor_id}",
    # response_model=CourseListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get courses by instructor",
    description="Retrieve a list of courses taught by a specific instructor.",
    # responses={
    #     200: {
    #         "description": "Instructor courses retrieved successfully",
    #         "model": CourseListResponse
    #     },
    #     404: {
    #         "description": "Instructor not found or has no courses",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "No courses found for this instructor"}
    #             }
    #         }
    #     }
    # }
)
async def get_courses_by_instructor(
    instructor_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Retrieve a list of courses taught by a specific instructor.

    This endpoint returns all courses that are associated with the specified instructor.

    - **instructor_id**: UUID of the instructor whose courses to retrieve
    """
    return course_service.get_intructor_course(
        instructor_id,
    )

@analysis_router.get(
    "/{course_id}",
    # response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get course analysis",
    description="Retrieve analytics and statistics for a specific course.",
    # responses={
    #     200: {
    #         "description": "Course analysis retrieved successfully",
    #         "content": {
    #             "application/json": {
    #                 "example": {
    #                     "detail": "Course analysis retrieved successfully",
    #                     "data": {
    #                         "course_id": "123e4567-e89b-12d3-a456-426614174000",
    #                         "total_enrollments": 150,
    #                         "completion_rate": 0.75,
    #                         "average_rating": 4.5,
    #                         "revenue": 14925.50,
    #                         "enrollment_trend": [
    #                             {"date": "2023-01", "count": 25},
    #                             {"date": "2023-02", "count": 35},
    #                             {"date": "2023-03", "count": 45}
    #                         ]
    #                     }
    #                 }
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Course not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def get_courses_analysis(
    course_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Retrieve analytics and statistics for a specific course.

    This endpoint returns detailed analytics about a course, including enrollment statistics,
    completion rates, revenue data, and other metrics useful for instructors and administrators.

    - **course_id**: UUID of the course to analyze
    """
    return course_service.get_courses_analysis(course_id)
