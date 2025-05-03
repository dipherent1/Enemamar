from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Course, Enrollment, Lesson
from app.domain.schema.courseSchema import CourseAnalysisResponse
from app.utils.exceptions.exceptions import NotFoundError, ValidationError
from sqlalchemy import or_
from typing import Optional
from app.repository.payment_repo import PaymentRepository
from app.repository.lesson_repo import LessonRepository

class CourseRepository:
    """
    Repository class for handling course-related database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the CourseRepository.

        Args:
            db (Session): The database session.
        """
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.lesson_repo = LessonRepository(db)

    def create_course(self, course: Course):
        """
        Create a new course in the database.

        Args:
            course (Course): The course object to be created.

        Returns:
            Course: The created course object.
        """
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def get_course_with_lessons(self, course_id: str):
        """
        Get a course with its lessons and instructor.

        Args:
            course_id (str): The ID of the course.

        Returns:
            Course: The course object with lessons and instructor loaded.

        Raises:
            NotFoundError: If the course is not found.
        """
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

    def get_course(self, course_id: str):
        """
        Get a course by its ID.

        Args:
            course_id (str): The ID of the course.

        Returns:
            Course: The course object with lessons and instructor loaded.
        """
        return self.get_course_with_lessons(course_id)

    def get_courses(self, page: int = 1, page_size: int = 10, search: Optional[str] = None, filter: Optional[str] = None):
        """
        Get all courses with pagination, search, and filter options.

        Args:
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.
            search (Optional[str], optional): Search term for course title, description, or tags. Defaults to None.
            filter (Optional[str], optional): Filter term for course tags. Defaults to None.

        Returns:
            List[Course]: A list of course objects.
        """
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

    def enroll_course(self, user_id: str, course_id: str):
        """
        Enroll a user in a course.

        Args:
            user_id (str): The ID of the user.
            course_id (str): The ID of the course.

        Returns:
            Enrollment: The created enrollment object.

        Raises:
            NotFoundError: If the course is not found.
        """
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise NotFoundError(detail="Course not found")

        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)

        return enrollment

    def get_enrolled_courses(self, user_id: str, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        """
        Get all courses enrolled by a user with pagination and search options.

        Args:
            user_id (str): The ID of the user.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.
            search (Optional[str], optional): Search term for course title or description. Defaults to None.

        Returns:
            List[Enrollment]: A list of enrollment objects with associated courses.
        """
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

    def get_enrolled_users(self, course_id: str, page: int = 1, page_size: int = 10):
        """
        Get all users enrolled in a course with pagination.

        Args:
            course_id (str): The ID of the course.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            List[Enrollment]: A list of enrollment objects.

        Raises:
            NotFoundError: If the course is not found.
        """
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

    def get_enrollment(self, user_id: str, course_id: str):
        """
        Get an enrollment by user ID and course ID.

        Args:
            user_id (str): The ID of the user.
            course_id (str): The ID of the course.

        Returns:
            Enrollment: The enrollment object.

        Raises:
            NotFoundError: If the enrollment is not found.
        """
        enrollment = (
            self.db.query(Enrollment)
            .filter(Enrollment.user_id == user_id)
            .filter(Enrollment.course_id == course_id)
            .first()
        )
        if not enrollment:
            return None
        return enrollment

    def get_enrolled_users_count(self, course_id: str) -> int:
        """
        Get the count of users enrolled in a course.

        Args:
            course_id (str): The ID of the course.

        Returns:
            int: The number of enrolled users.
        """
        return (
            self.db.query(Enrollment)
            .filter(Enrollment.course_id == course_id)
            .count()
        )

    def get_courses_by_instructor(self, instructor_id: str):
        """
        Get all courses by an instructor with course analysis.

        Args:
            instructor_id (str): The ID of the instructor.

        Returns:
            List[CourseAnalysisResponse]: A list of course analysis responses.
        """
        courses = self.db.query(Course).filter(Course.instructor_id == instructor_id).all()
        course_analysis_list = []
        for course in courses:
            analysis = self.course_analysis(course.id)
            course_analysis_list.append(analysis)
        return course_analysis_list
    
    def course_analysis(self, course_id: str):
        """
        Perform analysis on a course.

        Args:
            course_id (str): The ID of the course.

        Returns:
            CourseAnalysisResponse: The course analysis response.

        Raises:
            NotFoundError: If the course is not found.
        """
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
    
    def get_total_courses_count(self, search: Optional[str] = None, filter_tag: Optional[str] = None):
        """
        Get the total count of courses with search and filter options.

        Args:
            search (Optional[str], optional): Search term for course title or description. Defaults to None.
            filter_tag (Optional[str], optional): Filter term for course tags. Defaults to None.

        Returns:
            int: The total number of courses matching the criteria.
        """
        query = self.db.query(Course)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )

        if filter_tag:
            query = query.filter(Course.tags.ilike(f"%{filter_tag}%"))

        return query.count()

    def get_total_enrolled_users_count(self, course_id):
        """
        Get the total count of users enrolled in a course.

        Args:
            course_id: The ID of the course.

        Returns:
            int: The total number of enrolled users.
        """
        query = (
            self.db.query(Enrollment)
            .join(Course)
            .filter(Enrollment.course_id == course_id)
        )
        return query.count()

    def get_user_courses_count(self, user_id: str, search: Optional[str] = None):
        """
        Get the count of courses enrolled by a user with search option.

        Args:
            user_id (str): The ID of the user.
            search (Optional[str], optional): Search term for course title or description. Defaults to None.

        Returns:
            int: The number of courses enrolled by the user matching the criteria.
        """
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
    
    
    
    
    
    # def get_course_revenue(self, course_id: str):
    #     return self.payment_repo.get_course_revenue(course_id)

    # def get_lessons_count(self, course_id: str) -> int:
    #     return self.lesson_repo.get_lessons_count(course_id)
    
    # # Lesson methods are now in LessonRepository
    # def get_lessons(self, course_id: str, page: int = 1, page_size: int = 10):
    #     return self.lesson_repo.get_lessons(course_id, page, page_size)

    # def get_lesson_by_id(self, course_id: str, lesson_id: str):
    #     return self.lesson_repo.get_lesson_by_id(course_id, lesson_id)

    # def add_multiple_lessons(self, course_id: str, lessons: list[Lesson]):
    #     return self.lesson_repo.add_multiple_lessons(course_id, lessons)

    # def add_lesson(self, course_id: str, lesson: Lesson):
    #     return self.lesson_repo.add_lesson(course_id, lesson)

    # def edit_lesson(self, course_id: str, lesson_id: str, lesson_data: dict):
    #     return self.lesson_repo.edit_lesson(course_id, lesson_id, lesson_data)

    # def delete_lesson(self, course_id: str, lesson_id: str):
    #     return self.lesson_repo.delete_lesson(course_id, lesson_id)




    # # Video methods are now in LessonRepository
    # def add_video(self, video):
    #     return self.lesson_repo.add_video(video)

    # # Payment methods are now in PaymentRepository
    # def save_payment(self, payment):
    #     return self.payment_repo.save_payment(payment)

    # def get_payment(self, tx_ref: str):
    #     return self.payment_repo.get_payment(tx_ref)

    # def update_payment(self, tx_ref: str, status: str, ref_id: str):
    #     return self.payment_repo.update_payment(tx_ref, status, ref_id)

    # def get_user_payments(self, user_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
    #     return self.payment_repo.get_user_payments(user_id, page, page_size, filter)

    # def get_course_payments(self, course_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
    #     return self.payment_repo.get_course_payments(course_id, page, page_size, filter)

    # def get_lesson_video(self, lesson_id: str):
    #     return self.lesson_repo.get_lesson_video(lesson_id)

    # def get_video_by_id(self, lesson_id: str, video_id: str):
    #     # This method should be implemented in LessonRepository
    #     # For now, we'll just forward the call to the database
    #     from app.domain.model.course import Video
    #     video = (
    #         self.db.query(Video)
    #         .filter(Video.lesson_id == lesson_id)
    #         .filter(Video.id == video_id)
    #         .first()
    #     )
    #     if not video:
    #         raise NotFoundError(detail="Video not found")
    #     return video



    # #get course all by instructor


    # def get_user_payments_count(self, user_id: str, filter: Optional[str] = None):
    #     return self.payment_repo.get_user_payments_count(user_id, filter)

    # def get_course_payments_count(self, course_id: str, filter: Optional[str] = None):
    #     return self.payment_repo.get_course_payments_count(course_id, filter)

    

    



   
