from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Course, Enrollment
from app.domain.schema.courseSchema import CourseInput,CourseResponse,CreateCourseResponse,EnrollmentResponse,EnrollResponse, PaginationParams
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
    
    #get course by using course id
    def get_course(self, course_id: str):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        return course
    
    #get all courses
    def get_courses(self, page: int = 1, page_size: int = 10):
        #return the course and pagination data 
        return (
            self.db.query(Course)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )
    
    #enroll course by using user id and and course id 
    def enroll_course(self, user_id: str, course_id: str):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)

        
        return enrollment 
    
    #get all courses enrolled by user
    def get_courses_by_user(self, user_id: str, page: int = 1, page_size: int = 10):
        return (
            self.db.query(Enrollment)
            .options(joinedload(Enrollment.course))
            .filter(Enrollment.user_id == user_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    def get_user_courses_count(self, user_id: str):
        return (
            self.db.query(Enrollment)
            .filter(Enrollment.user_id == user_id)
            .count()
        )

    def get_total_courses_count(self):
        return self.db.query(Course).count()

    
