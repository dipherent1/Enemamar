from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Course, Enrollment, Lesson, Video
from app.utils.exceptions.exceptions import NotFoundError, ValidationError
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
    def get_enrolled_courses(self, user_id: str, page: int = 1, page_size: int = 10, search: Optional[str] = None):
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
    
    #get all users enrolled in a course
    def get_enrolled_users(self, course_id: str, page: int = 1, page_size: int = 10):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        return (
            self.db.query(Enrollment)
            .filter(Enrollment.course_id == course_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
    
    #get erollment by using user id and course id
    def get_enrollment(self, user_id: str, course_id: str):
        enrollment = (
            self.db.query(Enrollment)
            .filter(Enrollment.user_id == user_id)
            .filter(Enrollment.course_id == course_id)
            .first()
        )
        if not enrollment:
            return None
        return enrollment
    
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
   
    #add multiple lesson to course
    def add_multiple_lessons(self, course_id: str, lessons: list[Lesson]):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        # Add all lessons in a single operation
        self.db.add_all(lessons)
        self.db.commit()
        
        return lessons
    
    #add single lesson
    def add_lesson(self ,course_id:str ,lesson: Lesson):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
    
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)
        return lesson

    def get_enrolled_users_count(self, course_id: str) -> int:
        return (
            self.db.query(Enrollment)
            .filter(Enrollment.course_id == course_id)
            .count()
        )

    def add_video(self, video: Video):
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video
    


    def get_lesson_video(self, lesson_id: str):
        video = (
            self.db.query(Video)
            .filter(Video.lesson_id == lesson_id)
            .first()
        )
        return video

    def get_video_by_id(self, lesson_id: str, video_id: str):
        video = (
            self.db.query(Video)
            .filter(Video.lesson_id == lesson_id)
            .filter(Video.id == video_id)
            .first()
        )
        if not video:
            raise NotFoundError(detail="Video not found")
        return video

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


    
