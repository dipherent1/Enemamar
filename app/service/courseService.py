from app.utils.exceptions.exceptions import ValidationError, DuplicatedError, NotFoundError
import re
from app.domain.schema.courseSchema import CourseInput,CourseResponse,CreateCourseResponse,EnrollmentResponse,EnrollResponse
from app.domain.model.course import Course
from app.repository.courseRepo import CourseRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from app.utils.security.hash import hash_password, verify_password
from typing import Optional

class CourseService:
    def __init__(self, db):
        self.course_repo = CourseRepository(db)
    
    def addCourse(self, course_info: CourseInput):
        # Validate course name
        if not course_info.title:
            raise ValidationError(detail="Course name is required")
        
        # Convert course_info to Course ORM object
        course = Course(**course_info.model_dump(exclude_none=True))

        # Check for duplicate entry using database constraints
        try:
            course = self.course_repo.create_course(course)
        # Handle duplicate entry
        except IntegrityError:
            raise DuplicatedError(detail="Course with this name already exists")

        # Convert SQLAlchemy Course object to Pydantic Response Model
        course_response = CourseResponse.model_validate(course)
        
        # course_response = CourseResponse(
        #     id=course.id,
        #     title=course.title,
        #     price=course.price,
        #     description=course.description
        # )

        # Return response
        response = CreateCourseResponse(detail="Course created successfully", course=course_response)
        return response
    
    #get course by using course id
    def getCourse(self, course_id: str):
        # Validate course_id
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        # Get course
        course = self.course_repo.get_course(course_id)
        
        # Convert SQLAlchemy Course object to Pydantic Response Model
        course_response = CourseResponse.model_validate(course)
        
        # course_response = CourseResponse(
        #     id=course.id,
        #     title=course.title,
        #     price=course.price,
        #     description=course.description
        # )

        # Return response
        return {"detail": "course fetched successfully","course": course_response}
    
    #get all courses
    def getCourses(self, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        # Get paginated courses
        courses = self.course_repo.get_courses(page, page_size, search)
        
        # Convert to Pydantic models
        courses_response = [
            CourseResponse.model_validate(course)
            for course in courses
        ]

        # Return response with pagination metadata
        return {
            "detail": "Courses fetched successfully",
            "courses": courses_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.course_repo.get_total_courses_count(search)
            }
        }
    
    #enroll course by using user id and and course id
    def enrollCourse(self, user_id: str, course_id: str):
        # Validate user_id
        if not user_id:
            raise ValidationError(detail="User ID is required")
        
        # Validate course_id
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        # Enroll course
        enrollment = self.course_repo.enroll_course(user_id, course_id)
        
        # Convert SQLAlchemy Enrollment object to Pydantic Response Model
        enrollment_response = EnrollmentResponse.model_validate(enrollment)
        
        # enrollment_response = EnrollmentResponse(
        #     id=enrollment.id,
        #     user_id=enrollment.user_id,
        #     course_id=enrollment.course_id,
        #     # enrolled_at=enrollment.enrolled_at
        # )

        # Return response
        response = EnrollResponse(detail="Course enrolled successfully", enrollment=enrollment_response)
        return response
    
    #get all courses enrolled by user
    def getCoursesByUser(self, user_id: str, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        # Validate user_id
        if not user_id:
            raise ValidationError(detail="User ID is required")
        
        # Get paginated courses
        enrollments = self.course_repo.get_courses_by_user(user_id, page, page_size, search)
        
        # Extract and convert courses
        courses_response = [
            CourseResponse.model_validate(enrollment.course)
            for enrollment in enrollments
        ]

        # Return response with pagination metadata
        return {
            "detail": "User courses fetched successfully",
            "courses": courses_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.course_repo.get_user_courses_count(user_id, search)
            }
        }
def get_course_service(db: Session = Depends(get_db)):
    return CourseService(db)