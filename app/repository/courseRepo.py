from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Course, Enrollment, Module, Lesson
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
    
    #get course by using course id
    def get_course(self, course_id: str):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        return course
    
    #get all courses
    def get_courses(self, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        query = self.db.query(Course)
        
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
    
    #add module to course
    def add_module(self, course_id: str, module: Module):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        module.course_id = course_id
        self.db.add(module)
        self.db.commit()
        self.db.refresh(module)
        return module
    
    #get all modules of course
    def get_modules(self, course_id: str, page: int = 1, page_size: int = 10):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        return (
            self.db.query(Module)
            .filter(Module.course_id == course_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
    
    #get module by using module id
    def get_module(self, course_id: str, module_id: str):
        module = (
            self.db.query(Module)
            .filter(
                Module.id == module_id,
                Module.course_id == course_id
            )
            .first()
        )
        if not module:
            raise NotFoundError(detail="Module not found in this course")
        return module
    
    #add lesson to module
    def add_lesson(self, module_id: str, lesson: Lesson):
        # Verify module exists and belongs to course
        module = self.db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise NotFoundError(detail="Module not found")
        
        # Add lesson
        lesson.module_id = module_id
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)
        return lesson
    
    #get all lessons of module
    def get_lessons(self, module_id: str, page: int = 1, page_size: int = 10):
        # Verify module exists
        module = self.db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise NotFoundError(detail="Module not found")
        
        return (
            self.db.query(Lesson)
            .filter(Lesson.module_id == module_id)
            .order_by(Lesson.created_at.asc())  # Order by creation date
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    def get_lessons_count(self, module_id: str) -> int:
        return (
            self.db.query(Lesson)
            .filter(Lesson.module_id == module_id)
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

    def get_total_modules_count(self, course_id: str):
        return self.db.query(Module).filter(Module.course_id == course_id).count()
    
