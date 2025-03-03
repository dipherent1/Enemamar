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
        course_response = CourseResponse(
            id=course.id,
            title=course.title,
            price=course.price,
            description=course.description
        )

        # Return response
        response = CreateCourseResponse(detail="Course created successfully", course=course_response)
        return response
    
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
        enrollment_response = EnrollmentResponse(
            id=enrollment.id,
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            # enrolled_at=enrollment.enrolled_at
        )

        # Return response
        response = EnrollResponse(detail="Course enrolled successfully", enrollment=enrollment_response)
        return response
    

def get_course_service(db: Session = Depends(get_db)):
    return CourseService(db)