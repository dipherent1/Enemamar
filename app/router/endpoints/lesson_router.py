from fastapi import APIRouter, Depends
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

@lesson_router.get("/{course_id}")
async def get_lessons(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    search_params: PaginationParams = Depends(),
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Get all lessons for a course.
    
    Args:
        course_id (str): The course ID.
        decoded_token (dict): The decoded JWT token.
        search_params (PaginationParams): The pagination parameters.
        lesson_service (LessonService): The lesson service.
        
    Returns:
        dict: The lessons response.
    """
    user_id = decoded_token.get("id")
    return lesson_service.get_lessons(
        course_id,
        user_id,
        search_params.page,
        search_params.page_size
    )

@lesson_router.get("/{course_id}/{lesson_id}")
async def get_lesson_by_id(
    course_id: str,
    lesson_id: str,
    decoded_token: dict = Depends(is_logged_in),
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Get a lesson by ID.
    
    Args:
        course_id (str): The course ID.
        lesson_id (str): The lesson ID.
        decoded_token (dict): The decoded JWT token.
        lesson_service (LessonService): The lesson service.
        
    Returns:
        dict: The lesson response.
    """
    user_id = decoded_token.get("id")
    return lesson_service.get_lesson_by_id(course_id, lesson_id, user_id)

@protected_lesson_router.post("/{course_id}")
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

@protected_lesson_router.post("/{course_id}/{lesson_id}/video")
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

@protected_lesson_router.get("/{course_id}/{lesson_id}/video")
async def get_lesson_video(
    course_id: str,
    lesson_id: str,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Get the video for a lesson.
    
    Args:
        course_id (str): The course ID.
        lesson_id (str): The lesson ID.
        lesson_service (LessonService): The lesson service.
        
    Returns:
        dict: The video response.
    """
    return lesson_service.get_lesson_video(course_id, lesson_id)

@protected_lesson_router.put("/{course_id}/{lesson_id}")
async def edit_lesson(
    course_id: str,
    lesson_id: str,
    lesson_data: dict,
    lesson_service: LessonService = Depends(get_lesson_service)
):
    """
    Edit a lesson.
    
    Args:
        course_id (str): The course ID.
        lesson_id (str): The lesson ID.
        lesson_data (dict): The lesson data to update.
        lesson_service (LessonService): The lesson service.
        
    Returns:
        dict: The lesson response.
    """
    return lesson_service.edit_lesson(course_id, lesson_id, lesson_data)

@protected_lesson_router.delete("/{course_id}/{lesson_id}")
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
        dict: The lesson response.
    """
    return lesson_service.delete_lesson(course_id, lesson_id)
