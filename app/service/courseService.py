from app.utils.exceptions.exceptions import ValidationError
import re
from app.domain.schema.courseSchema import (
    CourseInput,
    CourseResponse,
    EnrollmentResponse,
    UserResponse,
    CourseAnalysisResponse,
)
from app.domain.model.course import Course, Enrollment
from app.repository.courseRepo import CourseRepository
from app.repository.lesson_repo import LessonRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from app.core.config.database import get_db
from typing import Optional
from app.repository.userRepo import UserRepository
from app.service.payment_service import PaymentService
from app.service.lesson_service import LessonService
from app.service.payment_service import PaymentService
from app.service.lesson_service import LessonService
from app.utils.bunny.bunnyStorage import BunnyCDNStorage
from app.core.config.env import get_settings
import os
from tempfile import NamedTemporaryFile


settings = get_settings()
class CourseService:
    def __init__(self, db):
        """
        Initialize the CourseService with the database session and repositories.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db
        self.course_repo = CourseRepository(db)
        self.user_repo = UserRepository(db)
        self.payment_service = PaymentService(db)
        self.lesson_service = LessonService(db)

    def addCourse(self, course_info: CourseInput):
        """
        Add a new course with optional lessons.

        Args:
            course_info (CourseInput): Input data for creating a course.

        Returns:
            dict: Response containing course creation details and data.

        Raises:
            ValidationError: If the instructor is invalid or course creation fails.
        """
        instructor = self.user_repo.get_user_by_id(str(course_info.instructor_id))
        if not instructor or not instructor.role == "instructor":
            raise ValidationError(detail="Invalid instructor ID or not an instructor")

        course_data = course_info.model_dump(exclude={'lessons'})
        course = Course(**course_data)
        created_course = self.course_repo.create_course(course)
        if not created_course:
            raise ValidationError(detail="Failed to create course")

        if course_info.lessons:
            self.lesson_service.add_multiple_lessons(str(created_course.id), course_info.lessons)

        created_course = self.course_repo.get_course_with_lessons(str(created_course.id))
        if not created_course:
            raise ValidationError(detail="Failed to fetch course with lessons")
        course_response = CourseResponse.model_validate(created_course)

        return {
            "detail": "Course created successfully",
            "data": course_response
        }
    
    def addThumbnail(self, course_id: str, thumbnail: UploadFile, thumbnail_name: str=""):
        """
        Add a thumbnail to a course.

        Args:
            course_id (str): ID of the course.
            thumbnail (UploadFile): Thumbnail file to upload.

        Returns:
            dict: Response containing thumbnail upload details.

        Raises:
            ValidationError: If the course ID is invalid or the thumbnail upload fails.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        course = self.course_repo.get_course(course_id)
        if not course:
            raise ValidationError(detail="Course not found")

        # Validate and save the thumbnail
        if not re.match(r"^image/(jpeg|png|jpg)$", thumbnail.content_type):
            raise ValidationError(detail="Invalid image format. Only JPEG and PNG are allowed.")

        try:
            # 1) Pass the correct storage zone, not the API key twice
            storage = BunnyCDNStorage(
                settings.BUNNY_CDN_THUMB_STORAGE_APIKEY,
                settings.BUNNY_CDN_THUMB_STORAGE_ZONE,
                settings.BUNNY_CDN_PULL_ZONE
            )

            # 2) Write UploadFile to a temp file so upload_file can open it by path
            from tempfile import NamedTemporaryFile

            # decide file_name
            file_name = thumbnail_name or thumbnail.filename

            with NamedTemporaryFile("wb", delete=False) as tmp:
                tmp.write(thumbnail.file.read())
                tmp_path = tmp.name

            # upload and then remove temp
            thumbnail_url = storage.upload_file(
                "",
                file_path=tmp_path,
                file_name=file_name
            )
            os.unlink(tmp_path)

            self.course_repo.save_thumbnail(course_id, thumbnail_url)
        except IntegrityError:
            raise ValidationError(detail="Failed to save thumbnail")

        return {
            "detail": "Thumbnail uploaded successfully",
            "data": {"thumbnail_url": thumbnail_url}
        }
    


    def getCourse(self, course_id: str):
        """
        Retrieve a course by its ID.

        Args:
            course_id (str): ID of the course to retrieve.

        Returns:
            dict: Response containing course details.

        Raises:
            ValidationError: If the course ID is invalid or the course is not found.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        course = self.course_repo.get_course_with_lessons(course_id)
        if not course:
            raise ValidationError(detail="Course not found")

        course_response = CourseResponse.model_validate(course)
        return {"detail": "course fetched successfully", "data": course_response}

    def getCourses(self, page: int = 1, page_size: int = 10, search: Optional[str] = None, filter: Optional[str] = None):
        """
        Retrieve a paginated list of courses.

        Args:
            page (int): Page number for pagination.
            page_size (int): Number of items per page.
            search (Optional[str]): Search query for filtering courses.
            filter (Optional[str]): Additional filter criteria.

        Returns:
            dict: Response containing paginated course data and metadata.
        """
        courses = self.course_repo.get_courses(page, page_size, search, filter)
        courses_response = [
            CourseResponse.model_validate(course).model_dump(exclude={'lessons'})
            for course in courses
        ]

        return {
            "detail": "Courses fetched successfully",
            "data": courses_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.course_repo.get_total_courses_count(search, filter)
            }
        }

    def getEnrollment(self, user_id: str, course_id: str):
        """
        Retrieve enrollment details for a user in a course.

        Args:
            user_id (str): ID of the user.
            course_id (str): ID of the course.

        Returns:
            dict: Response containing enrollment details.

        Raises:
            ValidationError: If the user or course ID is invalid or the user is not enrolled.
        """
        if not user_id:
            raise ValidationError(detail="User ID is required")
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        enrollment = self.course_repo.get_enrollment(user_id, course_id)
        if not enrollment:
            raise ValidationError(detail="User not enrolled in course")

        enrollment_response = EnrollmentResponse.model_validate(enrollment)
        return {"detail": "Enrollment fetched successfully", "data": enrollment_response}

    def enrollCourse(self, user_id: str, course_id: str):
        """
        Enroll a user in a course by initiating payment.

        Args:
            user_id (str): ID of the user.
            course_id (str): ID of the course.

        Returns:
            dict: Response from the payment service.
        """
        return self.payment_service.initiate_payment(user_id, course_id)

    # def enrollCourseCallback(self, payload):
    #     """
    #     Process the payment callback for course enrollment.

    #     Args:
    #         payload (dict): Callback payload data.

    #     Returns:
    #         dict: Response from the payment service.
    #     """
    #     return self.payment_service.process_payment_callback(payload)

    def getEnrolledCourses(self, user_id: str, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        """
        Retrieve a paginated list of courses a user is enrolled in.

        Args:
            user_id (str): ID of the user.
            page (int): Page number for pagination.
            page_size (int): Number of items per page.
            search (Optional[str]): Search query for filtering courses.

        Returns:
            dict: Response containing enrolled courses and pagination metadata.

        Raises:
            ValidationError: If the user ID is invalid.
        """
        if not user_id:
            raise ValidationError(detail="User ID is required")
        
        #check if user exists
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValidationError(detail="User not found")

        enrollments = self.course_repo.get_enrolled_courses(user_id, page, page_size, search)
        if not enrollments:
            return {
                "detail": "No courses found for the user",
                "data": [],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": 0
                }
            }

        courses_response = [
            CourseResponse.model_validate(enrollment.course).model_dump(exclude={'lessons'})
            for enrollment in enrollments
        ]

        return {
            "detail": "User courses fetched successfully",
            "data": courses_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.course_repo.get_user_courses_count(user_id, search)
            }
        }

    def getEnrolledUsers(
        self,
        course_id: str,
        year: Optional[int]     = None,
        month: Optional[int]    = None,
        week: Optional[int]     = None,
        day: Optional[int]      = None,
        page: Optional[int]     = None,
        page_size: Optional[int] = None,
    ):
        """
        Retrieve enrollments (not user info) for a course,
        filtered by created_at date and optionally paginated.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        enrollments = self.course_repo.get_enrolled_users(
            course_id=course_id,
            year=year, month=month, week=week, day=day,
            page=page, page_size=page_size
        )
        data = [EnrollmentResponse.model_validate(e) for e in enrollments]

        result = {
            "detail": "Course enrollments fetched successfully",
            "data": data
        }
        # only include pagination if requested
        if page is not None and page_size is not None:
            total = self.course_repo.get_enrolled_users_count(course_id)
            result["pagination"] = {
                "page": page,
                "page_size": page_size,
                "total_items": total
            }

        return result

    def get_courses_analysis(self, course_id: str):
        """
        Retrieve analysis data for a course.

        Args:
            course_id (str): ID of the course.

        Returns:
            dict: Response containing course analysis data.

        Raises:
            ValidationError: If the course ID is invalid.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        analysis_data = self.course_repo.course_analysis(course_id)
        if not analysis_data:
            return {
                "detail": "No analysis data found for this course",
                "data": None
            }

        return {
            "detail": "Course analysis fetched successfully",
            "data": analysis_data
        }

    def get_intructor_course(self, instructor_id: str):
        """
        Retrieve all courses created by an instructor.

        Args:
            instructor_id (str): ID of the instructor.

        Returns:
            dict: Response containing instructor's courses.

        Raises:
            ValidationError: If the instructor ID is invalid or the user is not an instructor.
        """
        if not instructor_id:
            raise ValidationError(detail="Instructor ID is required")

        user = self.user_repo.get_user_by_id(instructor_id)
        if not user or not user.role == "instructor":
            raise ValidationError(detail="Invalid instructor ID or not an instructor")

        courses = self.course_repo.get_courses_by_instructor(instructor_id)

        return {
            "detail": "Instructor courses fetched successfully",
            "data": courses
        }

    def is_user_enrolled(self, user_id: str, course_id: str) -> dict:
        """
        Check if a user is enrolled in a course.

        Raises ValidationError if inputs are missing.
        """
        if not user_id:
            raise ValidationError(detail="User ID is required")
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        enrolled = bool(self.course_repo.get_enrollment(str(user_id), course_id))
        return {
            "detail": "Enrollment status fetched successfully",
            "data": {"is_enrolled": enrolled}
        }


def get_course_service(db: Session = Depends(get_db)):
    return CourseService(db)