from fastapi import APIRouter, Depends, HTTPException
from app.domain.schema.authSchema import UpdateRoleRequest
from app.domain.schema.courseSchema import (
    CourseInput,
    CourseEditInput,
    LessonEditInput,
    VideoEditInput,
    SearchParams,
    MultipleLessonInput,
    VideoInput,
)
from app.service.userService import UserService, get_user_service
from app.service.courseService import CourseService, get_course_service
from app.service.lesson_service import LessonService, get_lesson_service
from app.service.payment_service import PaymentService, get_payment_service
from app.utils.middleware.dependancies import is_admin, is_admin_or_instructor

# Main admin router
admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(is_admin)]
)

# User management endpoints
@admin_router.get("/users")
async def get_all_users(
    params: SearchParams = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get all users.

    Args:
        params (SearchParams): The search parameters.
        user_service (UserService): The user service.

    Returns:
        dict: The users response.
    """
    return user_service.get_all_users(
        search=params.search,
        page=params.page,
        page_size=params.page_size,
        filter=params.filter
    )



@admin_router.put("/users/deactivate/{user_id}")
async def deactivate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Deactivate a user.

    Args:
        user_id (str): The user ID.
        user_service (UserService): The user service.

    Returns:
        dict: The deactivation response.
    """
    return user_service.deactivate_user(user_id)

@admin_router.put("/users/activate/{user_id}")
async def activate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Activate a user.

    Args:
        user_id (str): The user ID.
        user_service (UserService): The user service.

    Returns:
        dict: The activation response.
    """
    return user_service.activate_user(user_id)

@admin_router.put("/users/role/{user_id}")
async def update_user_role(
    user_id: str,
    role_request: UpdateRoleRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    Update a user's role.

    Args:
        user_id (str): The user ID.
        role_request (UpdateRoleRequest): The role update request.
        user_service (UserService): The user service.

    Returns:
        dict: The role update response.
    """
    return user_service.update_role(user_id, role_request.role)

# get courses enrolled by user
@admin_router.get("/user/{user_id}/enrolled")
async def get_users_enrolled_in_course(
    user_id: str,
    search_params: SearchParams = Depends(),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Retrieve all courses a specific user is enrolled in.

    Args:
        user_id (str): The ID of the user to query.
        search_params (SearchParams): Pagination and optional search filters.
        course_service (CourseService): Service for course-related operations.

    Returns:
        dict: Paginated list of courses the user is enrolled in,
              including metadata like total count, page, and page_size.
    """
    return course_service.getEnrolledCourses(
        user_id,
        search_params.page,
        search_params.page_size
    )

# Course management endpoints
@admin_router.post("/courses/add")
async def add_course(
    course_info: CourseInput,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Add a new course.

    Args:
        course_info (CourseInput): The course information.
        course_service (CourseService): The course service.

    Returns:
        dict: The course creation response.
    """
    return course_service.addCourse(course_info)

@admin_router.put("/courses/{course_id}")
async def update_course(
    course_id: str,
    course_info: CourseEditInput,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Update a course.

    Args:
        course_id (str): The course ID.
        course_info (CourseEditInput): The course information (without lessons).
        course_service (CourseService): The course service.

    Returns:
        dict: The course update response.
    """
    return course_service.updateCourse(course_id, course_info)

@admin_router.delete("/courses/{course_id}")
async def delete_course(
    course_id: str,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Delete a course.

    Args:
        course_id (str): The course ID.
        course_service (CourseService): The course service.

    Returns:
        dict: The course deletion response.
    """
    return course_service.deleteCourse(course_id)


####################################################


# Lesson management endpoints
@admin_router.post("/course/{course_id}/lessons")
async def add_multiple_lessons(
    course_id: str,
    lessons_input: MultipleLessonInput,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Add multiple lessons to a course.

    Args:
        course_id (str): The course ID.
        lessons_input (MultipleLessonInput): The lessons input.
        lesson_service (LessonService): The lesson service.

    Returns:
        dict: The lessons response.
    """
    return lesson_service.add_multiple_lessons(course_id, lessons_input)

@admin_router.post("/course/{course_id}/lessons/{lesson_id}/video")
async def add_video_to_lesson(
    course_id: str,
    lesson_id: str,
    video_input: VideoInput,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Add a video to a lesson.

    Args:
        course_id (str): The course ID.
        lesson_id (str): The lesson ID.
        video_input (VideoInput): The video input.
        lesson_service (LessonService): The lesson service.

    Returns:
        dict: The video response.
    """
    return lesson_service.add_video_to_lesson(course_id, lesson_id, video_input)

@admin_router.put("/course/{course_id}/lessons/{lesson_id}/video")
async def update_video(
    course_id: str,
    lesson_id: str,
    video_input: VideoEditInput,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Update a video for a lesson.

    Args:
        course_id (str): The course ID.
        lesson_id (str): The lesson ID.
        video_input (VideoEditInput): The video information to update.
        lesson_service (LessonService): The lesson service.

    Returns:
        dict: The video update response.
    """
    return lesson_service.edit_video(course_id, lesson_id, video_input)

@admin_router.put("/course/{course_id}/lessons/{lesson_id}")
async def update_lesson(
    course_id: str,
    lesson_id: str,
    lesson_input: LessonEditInput,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Update a lesson.

    Args:
        course_id (str): The course ID.
        lesson_id (str): The lesson ID.
        lesson_input (LessonEditInput): The lesson information (without video).
        lesson_service (LessonService): The lesson service.

    Returns:
        dict: The lesson update response.
    """
    return lesson_service.edit_lesson(course_id, lesson_id, lesson_input)



@admin_router.delete("/course/{course_id}/lessons/{lesson_id}")
async def delete_lesson(
    course_id: str,
    lesson_id: str,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Delete a lesson.

    Args:
        course_id (str): The course ID.
        lesson_id (str): The lesson ID.
        lesson_service (LessonService): The lesson service.

    Returns:
        dict: The lesson deletion response.
    """
    return lesson_service.delete_lesson(course_id, lesson_id)


# Payment management endpoints
# @admin_router.get("/payments")
# async def get_all_payments(
#     search_params: SearchParams = Depends(),
#     payment_service: PaymentService = Depends(get_payment_service)
# ):
#     """
#     Get all payments.

#     Args:
#         search_params (SearchParams): The search parameters.
#         payment_service (PaymentService): The payment service.

#     Returns:
#         dict: The payments response.
#     """
#     return payment_service.get_all_payments(
#         page=search_params.page,
#         page_size=search_params.page_size
#     )

@admin_router.get("/payments/{payment_id}")
async def get_payment(
    payment_id: str,
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Get a payment by ID.

    Args:
        payment_id (str): The payment ID.
        payment_service (PaymentService): The payment service.

    Returns:
        dict: The payment response.
    """
    return payment_service.get_payment(payment_id)

# Instructor management endpoints
# @admin_router.get("/instructors")
# async def get_all_instructors(
#     params: SearchParams = Depends(),
#     user_service: UserService = Depends(get_user_service)
# ):
#     """
#     Get all instructors.

#     Args:
#         params (SearchParams): The search parameters.
#         user_service (UserService): The user service.

#     Returns:
#         dict: The instructors response.
#     """
#     return user_service.get_all_instructors(
#         search=params.search,
#         page=params.page,
#         page_size=params.page_size
#     )

# @admin_router.get("/instructors/{instructor_id}")
# async def get_instructor_by_id(
#     instructor_id: str,
#     user_service: UserService = Depends(get_user_service)
# ):
#     """
#     Get an instructor by ID.

#     Args:
#         instructor_id (str): The instructor ID.
#         user_service (UserService): The user service.

#     Returns:
#         dict: The instructor response.
#     """
#     return user_service.get_instructor_by_id(instructor_id)


inst_admin_router = APIRouter(
    prefix="/inst-admin",
    tags=["admin"],
    dependencies=[Depends(is_admin_or_instructor)]
)

@inst_admin_router.get("/courses/{course_id}/enrolled")
async def get_users_enrolled_in_course(
    course_id: str,
    search_params: SearchParams = Depends(),
    course_service: CourseService = Depends(get_course_service),
    current_user: dict = Depends(is_admin_or_instructor)
):
    """
    Get all enrollments for a course, including full enrollment information.

    This endpoint returns detailed enrollment information for a specific course, including:
    - Enrollment ID
    - User ID of the enrolled student
    - Course ID
    - Enrollment date

    Authorization:
    - Admin users can access enrollment information for any course
    - Instructor users can only access enrollment information for courses assigned to them

    Args:
        course_id (str): The ID of the course to get enrollments for
        search_params (SearchParams): Pagination parameters (page, page_size)
        course_service (CourseService): Service for course-related operations
        current_user (dict): The current authenticated user information

    Returns:
        dict: Response containing:
            - detail: Success message
            - data: List of enrollment objects with complete enrollment information
            - pagination: Metadata including page, page_size, and total_items

    Raises:
        HTTPException:
            - 403 Forbidden if an instructor tries to access a course not assigned to them
            - 404 Not Found if the course doesn't exist
    """
    # If user is an admin, allow access to any course
    if current_user.get("role") == "admin":
        return course_service.getEnrolledUsers(
            course_id,
            search_params.page,
            search_params.page_size
        )

    # For instructors, verify the course belongs to them
    try:
        course = course_service.course_repo.get_course(course_id)
        if str(course.instructor_id) != current_user.get("id"):
            raise HTTPException(
                status_code=403,
                detail="Instructors can only access enrollment information for their own courses"
            )
    except Exception:
        # If course doesn't exist or there's another error, return a 404
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course_service.getEnrolledUsers(
        course_id,
        search_params.page,
        search_params.page_size
    )
