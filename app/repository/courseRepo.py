from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Course, Enrollment, Lesson
from app.domain.schema.courseSchema import (
    CourseInput,
    CourseResponse,
    CreateCourseResponse,
    EnrollmentResponse,
    EnrollResponse,
    PaginationParams,
    CourseSearchParams,
    ModuleInput,
    ModuleResponse
)
from app.utils.exceptions.exceptions import ValidationError, DuplicatedError, NotFoundError
from app.utils.security.jwt_handler import create_access_token, create_refresh_token
from sqlalchemy import or_, func
from typing import Optional

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_course(self, course: Course):
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def get_course_with_lessons(self, course_id: str):
        course = (
            self.db.query(Course)
            .options(
                joinedload(Course.lessons),
                joinedload(Course.instructor)
            )
            .filter(Course.id == course_id)
            .first()
        )
        if not course:
            raise NotFoundError(detail="Course not found")
        return course

    #get course by using course id
    def get_course(self, course_id: str):
        return self.get_course_with_lessons(course_id)
    
    #get all courses
    def get_courses(self, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        query = (
            self.db.query(Course)
            .options(
                joinedload(Course.instructor)  # Only load instructor relationship
            )
        )
        
        if search:
            # Fuzzy search using ILIKE for case-insensitive matching
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )
        
        return (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
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
    def get_courses_by_user(self, user_id: str, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        query = (
            self.db.query(Enrollment)
            .options(joinedload(Enrollment.course))
            .filter(Enrollment.user_id == user_id)
        )
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )
        
        return (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    
    #add lesson to course
    def add_lesson(self, course_id: str, lesson: Lesson):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        lesson.course_id = course_id
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)
        return lesson
    
    #get all lessons of course
    def get_lessons(self, course_id: str, page: int = 1, page_size: int = 10):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        return (
            self.db.query(Lesson)
            .filter(Lesson.course_id == course_id)
            .order_by(Lesson.created_at.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
    
    #get lesson by id
    def get_lesson_by_id(self, course_id: str, lesson_id: str):
        lesson = (
            self.db.query(Lesson)
            .filter(Lesson.course_id == course_id)
            .filter(Lesson.id == lesson_id)
            .first()
        )
        if not lesson:
            raise NotFoundError(detail="Lesson not found")
        return lesson

    def get_lessons_count(self, course_id: str) -> int:
        return (
            self.db.query(Lesson)
            .filter(Lesson.course_id == course_id)
            .count()
        )

    def get_user_courses_count(self, user_id: str, search: Optional[str] = None):
        query = (
            self.db.query(Enrollment)
            .join(Course)
            .filter(Enrollment.user_id == user_id)
        )
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )
        
        return query.count()

    def get_total_courses_count(self, search: Optional[str] = None):
        query = self.db.query(Course)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )
        
        return query.count()

    def add_multiple_lessons(self, course_id: str, lessons: list[Lesson]):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        for lesson in lessons:
            lesson.course_id = course_id
            self.db.add(lesson)
        
        self.db.commit()
        return lessons

    
