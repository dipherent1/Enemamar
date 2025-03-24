from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Course, Enrollment, Lesson, Video, Payment
from app.domain.schema.courseSchema import CourseAnalysisResponse
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
    def get_courses(self, page: int = 1, page_size: int = 10, search: Optional[str] = None, filter: Optional[str] = None):
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
                    Course.description.ilike(search_term),
                    Course.tags.ilike(search_term)
                )
            )

        if filter:
            query = query.filter(Course.tags.ilike(f"%{filter}%"))
        
        return (
            query
            .offset((page - 1) * page_size)  # Pagination offset
            .limit(page_size)  # Limit results to page size
            .all()
        )
    
    #enroll course by using user id and course id 
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
        """
        Retrieve all lessons for a given course.

        Args:
            course_id (str): The ID of the course.
            page (int, optional): The page number for pagination. Defaults to 1.
            page_size (int, optional): The number of lessons per page. Defaults to 10.

        Returns:
            List[Lesson]: A list of lessons for the specified course.
        """
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        return (
            self.db.query(Lesson)
            .filter(Lesson.course_id == course_id)
            .order_by(Lesson.order.asc())  # Order lessons in ascending order
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
    def add_lesson(self, course_id: str, lesson: Lesson):
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
    
    def save_payment(self, payment: Payment):
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
    
    def get_payment(self, tx_ref: str):
        payment = (
            self.db.query(Payment)
            .filter(Payment.tx_ref == tx_ref)
            .first()
        )
        if not payment:
            return None
        return payment
    
    def update_payment(self, tx_ref: str, status: str, ref_id: str):
        payment = self.get_payment(tx_ref)
        if not payment:
            raise NotFoundError(detail="Payment not found")
        
        payment.status = status
        payment.ref_id = ref_id
        self.db.commit()
        self.db.refresh(payment)
        return payment

    #get user payment with pagination and sorting
    def get_user_payments(self, user_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        query = (
            self.db.query(Payment)
            .filter(Payment.user_id == user_id)
        )
        
        if filter:
            query = query.filter(Payment.status == filter)
        
        payments = (
            query
            .order_by(Payment.updated_at.desc())  # Sort by updated_at in descending order
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return payments
    
    #get course payment
    def get_course_payments(self, course_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        query = (
            self.db.query(Payment)
            .filter(Payment.course_id == course_id)
        )
        
        if filter:
            query = query.filter(Payment.status == filter)
        
        payments = (
            query
            .order_by(Payment.updated_at.desc())  # Sort by updated_at in descending order
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return payments

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
    
    def course_analysis(self, course_id: str):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")
        
        total_lessons = self.get_lessons_count(course_id)
        total_enrolled_users = self.get_total_enrolled_users_count(course_id)
        
        for lesson in course.lessons:
            lesson.video = None

        return CourseAnalysisResponse(
            course=course,
            view_count=course.view_count,
            no_of_enrollments=total_enrolled_users,
            no_of_lessons=total_lessons,
            revenue=self.get_course_revenue(course_id)
        )
    
    #get course all by instructor
    def get_courses_by_instructor(self, instructor_id: str):
        courses = self.db.query(Course).filter(Course.instructor_id == instructor_id).all()
        course_analysis_list = []
        for course in courses:
            analysis = self.course_analysis(course.id)
            course_analysis_list.append(analysis)
        return course_analysis_list

    def get_user_payments_count(self, user_id: str, filter: Optional[str] = None):
        query = self.db.query(Payment).filter(Payment.user_id == user_id)
        if filter is not None:
            query = query.filter(Payment.status == filter)
        return query.count()

    def get_course_payments_count(self, course_id: str, filter: Optional[str] = None):
        query = self.db.query(Payment).filter(Payment.course_id == course_id)
        if filter is not None:
            query = query.filter(Payment.status == filter)
        return query.count()

    def get_course_revenue(self, course_id: str):
        total_revenue = (
            self.db.query(func.sum(Payment.amount))
            .filter(Payment.course_id == course_id)
            .filter(Payment.status == "success")
            .scalar()
        )
        return total_revenue or 0.0

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

    def get_total_courses_count(self, search: Optional[str] = None, filter: Optional[str] = None):
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

    def get_total_enrolled_users_count(self, course_id):
        query = (
            self.db.query(Enrollment)
            .join(Course)
            .filter(Enrollment.course_id == course_id)
        )
        return query.count()

