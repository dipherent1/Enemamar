from fastapi import APIRouter, Depends, status
from app.domain.schema.courseSchema import (
    PaginationParams,
    MultipleLessonInput,
    VideoInput,
)
from app.service.lesson_service import LessonService, get_lesson_service
from app.utils.middleware.dependancies import is_admin, is_logged_in

# Public lesson router
lesson_router = APIRouter(
    prefix="/lesson",
    tags=["lesson"]
)

# Protected lesson router (admin only)
protected_lesson_router = APIRouter(
    prefix="/protected/lesson",
    tags=["lesson"],
    dependencies=[Depends(is_admin)]
)

@lesson_router.get(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Get all lessons for a course",
    description="Retrieve a paginated list of all lessons for a specific course with generated video URLs."
)
async def get_lessons(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    search_params: PaginationParams = Depends(),
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Retrieve a paginated list of all lessons for a specific course.

    This endpoint returns all lessons associated with the specified course,
    with pagination support. The user must be enrolled in the course to access its lessons.

    - **course_id**: UUID of the course whose lessons to retrieve
    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    return lesson_service.get_lessons(
        course_id,
        user_id,
        search_params.page,
        search_params.page_size
    )

@lesson_router.get(
    "/{course_id}/{lesson_id}",
    status_code=status.HTTP_200_OK,
    summary="Get lesson by ID",
    description="Retrieve detailed information about a specific lesson with generated video URL."
)
async def get_lesson_by_id(
    course_id: str,
    lesson_id: str,
    decoded_token: dict = Depends(is_logged_in),
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Retrieve detailed information about a specific lesson.

    This endpoint returns comprehensive details about a lesson, including its content,
    video URL (if available), and other metadata. The user must be enrolled in the course
    to access its lessons.

    - **course_id**: UUID of the course containing the lesson
    - **lesson_id**: UUID of the lesson to retrieve

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    return lesson_service.get_lesson_by_id(course_id, lesson_id, user_id)

@protected_lesson_router.post(
    "/{course_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add multiple lessons to a course",
    description="Create multiple lessons for a course, optionally with video information."
)
async def add_multiple_lessons(
    course_id: str,
    lessons_input: MultipleLessonInput,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Add multiple lessons to a course at once.

    This endpoint allows creating multiple lessons for a course in a single request.
    Each lesson can optionally include video information, which will be stored in the
    video table and linked to the lesson. The video URL is not stored directly but
    will be generated when the lesson is retrieved.

    - **course_id**: UUID of the course to add lessons to
    - **lessons_input**: Object containing an array of lesson objects:
      - **title**: The lesson title
      - **description**: The lesson description
      - **duration**: The lesson duration in minutes
      - **order**: The lesson order in the course (optional)
      - **video**: Optional video metadata object:
        - **video_id**: The video ID from the video hosting service
        - **library_id**: The library ID from the video hosting service
        - **secret_key**: The secret key for generating secure URLs

    If video information is provided, the secret key will be encrypted before storage.
    """
    return lesson_service.add_multiple_lessons(course_id, lessons_input)

@protected_lesson_router.post(
    "/{course_id}/{lesson_id}/video",
    status_code=status.HTTP_201_CREATED,
    summary="Add video to lesson",
    description="Add video information to a lesson for generating secure video URLs."
)
async def add_video_to_lesson(
    course_id: str,
    lesson_id: str,
    video_input: VideoInput,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Add video information to a lesson for generating secure video URLs.

    This endpoint stores the video metadata (video_id, library_id, secret_key) that will be used
    to generate secure video URLs when the lesson is retrieved. The actual video URL is not stored
    but generated dynamically when the lesson is accessed.

    - **course_id**: UUID of the course containing the lesson
    - **lesson_id**: UUID of the lesson to add the video to
    - **video_input**: Object containing video metadata:
      - **video_id**: The video ID from the video hosting service
      - **library_id**: The library ID from the video hosting service
      - **secret_key**: The secret key for generating secure URLs

    The secret key will be encrypted before storage for security.
    """
    return lesson_service.add_video_to_lesson(course_id, lesson_id, video_input)

@protected_lesson_router.get(
    "/{course_id}/{lesson_id}/video",
    status_code=status.HTTP_200_OK,
    summary="Get video metadata for a lesson",
    description="Retrieve the video metadata associated with a lesson (not the generated URL)."
)
async def get_lesson_video(
    course_id: str,
    lesson_id: str,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Retrieve the video metadata associated with a lesson.

    This endpoint returns the raw video metadata stored in the database, not the generated
    video URL. The metadata includes the video_id, library_id, and encrypted secret_key
    that are used to generate the secure video URL when a lesson is accessed.

    - **course_id**: UUID of the course containing the lesson
    - **lesson_id**: UUID of the lesson whose video metadata to retrieve

    Note: This endpoint is for administrative purposes. To get a lesson with its
    generated video URL, use the regular lesson retrieval endpoint.
    """
    return lesson_service.get_lesson_video(course_id, lesson_id)

@protected_lesson_router.put(
    "/{course_id}/{lesson_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a lesson",
    description="Update a lesson's information (does not affect video metadata)."
)
async def edit_lesson(
    course_id: str,
    lesson_id: str,
    lesson_data: dict,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Update a lesson's information.

    This endpoint allows updating a lesson's basic information such as title, description,
    duration, and order. It does not modify the associated video metadata - use the
    dedicated video endpoints for that purpose.

    - **course_id**: UUID of the course containing the lesson
    - **lesson_id**: UUID of the lesson to update
    - **lesson_data**: Object containing the fields to update:
      - **title**: The lesson title (optional)
      - **description**: The lesson description (optional)
      - **duration**: The lesson duration in minutes (optional)
      - **order**: The lesson order in the course (optional)

    Only the fields included in the request will be updated.
    """
    return lesson_service.edit_lesson(course_id, lesson_id, lesson_data)

@protected_lesson_router.delete(
    "/{course_id}/{lesson_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a lesson",
    description="Delete a lesson and its associated video metadata."
)
async def delete_lesson(
    course_id: str,
    lesson_id: str,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Delete a lesson and its associated video metadata.

    This endpoint permanently removes a lesson from a course, including any
    associated video metadata. This operation cannot be undone.

    - **course_id**: UUID of the course containing the lesson
    - **lesson_id**: UUID of the lesson to delete

    Note: This will also delete any video metadata associated with the lesson.
    """
    return lesson_service.delete_lesson(course_id, lesson_id)
