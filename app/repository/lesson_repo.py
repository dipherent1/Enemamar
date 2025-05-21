from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Lesson, Video, Course
from app.utils.exceptions.exceptions import NotFoundError
from typing import List, Tuple, Optional, Any

def _wrap_return(result: Any) -> Tuple[Any, None]:
    return result, None
def _wrap_error(e: Exception) -> Tuple[None, Exception]:
    return None, e

class LessonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_lessons(self, course_id: str, page: int = 1, page_size: int = 10):
        """
        Retrieve all lessons for a given course.

        Args:
            course_id (str): The ID of the course.
            page (int, optional): The page number for pagination. Defaults to 1.
            page_size (int, optional): The number of lessons per page. Defaults to 10.

        Returns:
            List[Lesson]: A list of lessons for the specified course.

        Raises:
            NotFoundError: If the course is not found.
        """
        try:
            course = self.db.query(Course).filter(Course.id == course_id).first()
            if not course:
                return None, None
            lessons = (
                self.db.query(Lesson)
                .filter(Lesson.course_id == course_id)
                .order_by(Lesson.order.asc())
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
            return _wrap_return(lessons)
        except Exception as e:
            return _wrap_error(e)

    def get_lesson_by_id(self, course_id: str, lesson_id: str):
        """
        Get a lesson by ID.

        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.

        Returns:
            Lesson: The lesson object.

        Raises:
            NotFoundError: If the lesson is not found.
        """
        try:
            lesson = (
                self.db.query(Lesson)
                .filter(Lesson.course_id == course_id)
                .filter(Lesson.id == lesson_id)
                .first()
            )
            if not lesson:
                return None, None
            return _wrap_return(lesson)
        except Exception as e:
            return _wrap_error(e)

    def add_multiple_lessons(self, course_id: str, lessons: List[Lesson]):
        """
        Add multiple lessons to a course.

        Args:
            course_id (str): The course ID.
            lessons (List[Lesson]): The list of lesson objects.

        Returns:
            List[Lesson]: The list of added lesson objects.

        Raises:
            NotFoundError: If the course is not found.
        """
        try:
            course = self.db.query(Course).filter(Course.id == course_id).first()
            if not course:
                return None, None
            self.db.add_all(lessons)
            self.db.commit()
            return _wrap_return(lessons)
        except Exception as e:
            return _wrap_error(e)

    def add_lesson(self, course_id: str, lesson: Lesson):
        """
        Add a single lesson to a course.

        Args:
            course_id (str): The course ID.
            lesson (Lesson): The lesson object.

        Returns:
            Lesson: The added lesson object.

        Raises:
            NotFoundError: If the course is not found.
        """
        try:
            course = self.db.query(Course).filter(Course.id == course_id).first()
            if not course:
                return None, None
            self.db.add(lesson)
            self.db.commit()
            self.db.refresh(lesson)
            return _wrap_return(lesson)
        except Exception as e:
            return _wrap_error(e)

    def edit_lesson(self, course_id: str, lesson_id: str, lesson_data: dict):
        """
        Edit a lesson.

        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.
            lesson_data (dict): The lesson data to update.

        Returns:
            Lesson: The updated lesson object.

        Raises:
            NotFoundError: If the lesson is not found.
        """
        try:
            lesson_to_update = (
                self.db.query(Lesson)
                .filter(Lesson.course_id == course_id)
                .filter(Lesson.id == lesson_id)
                .first()
            )
            if not lesson_to_update:
                return None, None
            for key, value in lesson_data.items():
                if hasattr(lesson_to_update, key):
                    setattr(lesson_to_update, key, value)
            self.db.commit()
            self.db.refresh(lesson_to_update)
            return _wrap_return(lesson_to_update)
        except Exception as e:
            return _wrap_error(e)

    def delete_lesson(self, course_id: str, lesson_id: str):
        """
        Delete a lesson.

        Args:
            course_id (str): The course ID.
            lesson_id (str): The lesson ID.

        Returns:
            Lesson: The deleted lesson object.

        Raises:
            NotFoundError: If the lesson is not found.
        """
        try:
            lesson_to_delete = (
                self.db.query(Lesson)
                .filter(Lesson.course_id == course_id)
                .filter(Lesson.id == lesson_id)
                .first()
            )
            if not lesson_to_delete:
                return None, None
            self.db.delete(lesson_to_delete)
            self.db.commit()
            return _wrap_return(lesson_to_delete)
        except Exception as e:
            return _wrap_error(e)

    def get_lessons_count(self, course_id: str) -> int:
        """
        Get the count of lessons for a course.

        Args:
            course_id (str): The course ID.

        Returns:
            int: The count of lessons.
        """
        try:
            count = self.db.query(Lesson).filter(Lesson.course_id == course_id).count()
            return _wrap_return(count)
        except Exception as e:
            return _wrap_error(e)

    def add_video(self, video: Video):
        """
        Add a video to a lesson.

        Args:
            video (Video): The video object.

        Returns:
            Video: The added video object.
        """
        try:
            self.db.add(video)
            self.db.commit()
            self.db.refresh(video)
            return _wrap_return(video)
        except Exception as e:
            return _wrap_error(e)

    def get_lesson_video(self, lesson_id: str):
        """
        Get the video for a lesson.

        Args:
            lesson_id (str): The lesson ID.

        Returns:
            Video: The video object if found, None otherwise.
        """
        try:
            video = (
                self.db.query(Video)
                .filter(Video.lesson_id == lesson_id)
                .first()
            )
            return _wrap_return(video)
        except Exception as e:
            return _wrap_error(e)

    def get_lesson_video_by_id(self, video_id: str):
        """
        Get a video by its ID.

        Args:
            video_id (str): The video ID.

        Returns:
            Video: The video object if found, None otherwise.
        """
        try:
            video = (
                self.db.query(Video)
                .filter(Video.id == video_id)
                .first()
            )
            if not video:
                return None, None
            return _wrap_return(video)
        except Exception as e:
            return _wrap_error(e)

    def delete_video(self, video_id: str):
        """
        Delete a video.

        Args:
            video_id (str): The video ID.

        Returns:
            Video: The deleted video object.

        Raises:
            NotFoundError: If the video is not found.
        """
        try:
            video_to_delete = (
                self.db.query(Video)
                .filter(Video.id == video_id)
                .first()
            )
            if not video_to_delete:
                return None, None
            self.db.delete(video_to_delete)
            self.db.commit()
            return _wrap_return(video_to_delete)
        except Exception as e:
            return _wrap_error(e)

    def edit_video(self, video_id: str, video_data: dict):
        """
        Edit a video.

        Args:
            video_id (str): The video ID.
            video_data (dict): The video data to update.

        Returns:
            Video: The updated video object.

        Raises:
            NotFoundError: If the video is not found.
        """
        try:
            video_to_update = (
                self.db.query(Video)
                .filter(Video.id == video_id)
                .first()
            )
            if not video_to_update:
                return None, None
            for key, value in video_data.items():
                if hasattr(video_to_update, key):
                    setattr(video_to_update, key, value)
            self.db.commit()
            self.db.refresh(video_to_update)
            return _wrap_return(video_to_update)
        except Exception as e:
            return _wrap_error(e)
