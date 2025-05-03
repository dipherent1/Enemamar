from app.utils.exceptions.exceptions import ValidationError
from app.domain.schema.courseSchema import (
    LessonResponse,
    VideoInput,
    videoResponse,
    MultipleLessonInput,
)
from app.domain.model.course import Lesson, Video
from app.repository.lesson_repo import LessonRepository
from app.repository.courseRepo import CourseRepository
from app.repository.userRepo import UserRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from app.utils.bunny.bunny import generate_secure_bunny_stream_url, encrypt_secret_key, decrypt_secret_key

class LessonService:
    def __init__(self, db: Session):
        self.lesson_repo = LessonRepository(db)
        self.course_repo = CourseRepository(db)
        self.user_repo = UserRepository(db)
    
    def check_lesson_access(self, course_id, user_id):
        """
        Check if a user has access to a course's lessons.
        
        Args:
            course_id: The course ID.
            user_id: The user ID.
            
        Returns:
            bool: True if the user has access, False otherwise.
            
        Raises:
            ValidationError: If the user is not found or not enrolled in the course.
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValidationError(detail="User not found")
        
        # Check if user is enrolled in course
        enrollment = self.course_repo.get_enrollment(user_id, course_id)
        if not enrollment and user.role not in ["instructor", "admin"]:
            raise ValidationError(detail="User not enrolled in course")
        return True
    
    def get_lessons(self, course_id: str, user_id, page: int = 1, page_size: int = 10):
        """
        Get all lessons for a course.
        
        Args:
            course_id (str): The course ID.
            user_id: The user ID.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The page size. Defaults to 10.
            
        Returns:
            dict: The lessons response.
        """
        self.check_lesson_access(course_id, user_id)
        lessons = self.lesson_repo.get_lessons(course_id, page, page_size)
        lessons_response = [
            LessonResponse.model_validate(lesson)
            for lesson in lessons
        ]
        
        return {
            "detail": "Lessons fetched successfully",
            "data": lessons_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.lesson_repo.get_lessons_count(course_id)
            }
        }
    
    def get_lesson_by_id(self, course_id: str, lesson_id: str, user_id: str):
        """
        Get a lesson by ID.
        
        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.
            user_id (str): The user ID.
            
        Returns:
            dict: The lesson response.
            
        Raises:
            ValidationError: If the course ID or lesson ID is not provided.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        if not lesson_id:
            raise ValidationError(detail="Lesson ID is required")
        
        self.check_lesson_access(course_id, user_id)

        lesson = self.lesson_repo.get_lesson_by_id(course_id, lesson_id)
        lesson_response = LessonResponse.model_validate(lesson)

        video = self.lesson_repo.get_lesson_video(lesson_id)
        if video:
            video_response = videoResponse.model_validate(video)
            library_id, video_id, secret_key = video_response.library_id, video_response.video_id, video_response.secret_key
            
            if secret_key:
                try:
                    secret_key = decrypt_secret_key(secret_key)
                except Exception as e:
                    raise ValidationError(detail=f"Failed to decrypt video secret key: {str(e)}")
            
            url = generate_secure_bunny_stream_url(library_id, video_id, secret_key)
            lesson_response.video_url = url
        
        return {
            "detail": "Lesson fetched successfully",
            "data": lesson_response
        }
    
    def add_multiple_lessons_helper(self, course_id: str, lessons_input):
        """
        Helper method to add multiple lessons to a course.
        
        Args:
            course_id (str): The course ID.
            lessons_input: The lessons input.
            
        Returns:
            list: The list of added lesson responses.
            
        Raises:
            ValidationError: If the course ID is not provided or adding a lesson fails.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        lessons_responses = []
        for lesson in lessons_input:
            lesson_data = Lesson(**lesson.model_dump(exclude={'video'}))
            lesson_data.course_id = course_id

            try:
                created_lesson = self.lesson_repo.add_lesson(course_id, lesson_data)
            except IntegrityError as e:
                raise ValidationError(detail=f"Failed to add lesson, {str(e)}")
            
            lesson_response = LessonResponse.model_validate(created_lesson)
            lessons_responses.append(lesson_response)

            if lesson.video:
                self.add_video_to_lesson_helper(course_id, created_lesson.id, lesson.video)
                
        return lessons_responses
    
    def add_multiple_lessons(self, course_id: str, lessons_input: MultipleLessonInput):
        """
        Add multiple lessons to a course.
        
        Args:
            course_id (str): The course ID.
            lessons_input (MultipleLessonInput): The lessons input.
            
        Returns:
            dict: The lessons response.
        """
        return {
            "detail": "Lessons added successfully",
            "data": self.add_multiple_lessons_helper(course_id, lessons_input.lessons)
        }

    def add_video_to_lesson_helper(self, course_id: str, lesson_id: str, video_input: VideoInput):
        """
        Helper method to add a video to a lesson.
        
        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.
            video_input (VideoInput): The video input.
            
        Returns:
            Video: The added video object.
            
        Raises:
            ValidationError: If the lesson is not found or adding the video fails.
        """
        # Get lesson and check if available
        lesson = self.lesson_repo.get_lesson_by_id(course_id, lesson_id)  
        if not lesson:
            raise ValidationError(detail="Lesson not found")
        
        # Create video
        video_input.secret_key = encrypt_secret_key(video_input.secret_key)
        video_data = video_input.model_dump()
        video = Video(**video_data, lesson_id=lesson_id)
        
        # Add video to lesson
        try:
            created_video = self.lesson_repo.add_video(video)
        except IntegrityError:
            raise ValidationError(detail="Failed to add video, video already exists")
        
        return created_video
        
    def add_video_to_lesson(self, course_id: str, lesson_id: str, video_input: VideoInput):
        """
        Add a video to a lesson.
        
        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.
            video_input (VideoInput): The video input.
            
        Returns:
            dict: The video response.
        """
        created_video = self.add_video_to_lesson_helper(course_id, lesson_id, video_input)
        return {
            "detail": "Video added successfully",
            "data": created_video
        }

    def get_lesson_video(self, course_id: str, lesson_id: str):
        """
        Get the video for a lesson.
        
        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.
            
        Returns:
            dict: The video response.
        """
        video = self.lesson_repo.get_lesson_video(lesson_id)
        if not video:
            return {
                "detail": "No video found for this lesson",
                "data": None
            }
            
        return {
            "detail": "Video fetched successfully",
            "data": videoResponse.model_validate(video)
        }
    
    def edit_lesson(self, course_id: str, lesson_id: str, lesson_data: dict):
        """
        Edit a lesson.
        
        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.
            lesson_data (dict): The lesson data to update.
            
        Returns:
            dict: The lesson response.
        """
        updated_lesson = self.lesson_repo.edit_lesson(course_id, lesson_id, lesson_data)
        return {
            "detail": "Lesson updated successfully",
            "data": LessonResponse.model_validate(updated_lesson)
        }
    
    def delete_lesson(self, course_id: str, lesson_id: str):
        """
        Delete a lesson.
        
        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.
            
        Returns:
            dict: The lesson response.
        """
        deleted_lesson = self.lesson_repo.delete_lesson(course_id, lesson_id)
        return {
            "detail": "Lesson deleted successfully",
            "data": LessonResponse.model_validate(deleted_lesson)
        }

def get_lesson_service(db: Session = Depends(get_db)) -> LessonService:
    """
    Get a LessonService instance.
    
    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        
    Returns:
        LessonService: A LessonService instance.
    """
    return LessonService(db)
