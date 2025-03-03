from sqlalchemy.orm import Session
from app.domain.model.course import Course
from app.domain.schema.courseSchema import CourseInput,CourseResponse,CreateCourseResponse,EnrollmentResponse,EnrollResponse
from app.utils.exceptions.exceptions import ValidationError, DuplicatedError, NotFoundError
from app.utils.security.jwt_handler import create_access_token, create_refresh_token

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_course(self, course: Course):
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course
    
    
