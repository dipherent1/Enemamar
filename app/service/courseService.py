from app.utils.exceptions.exceptions import ValidationError
import re
from app.domain.schema.courseSchema import (
    CourseInput,
    CourseResponse,
    EnrollmentResponse,
    PaymentData,
    PaymentResponse,
    LessonResponse,
    UserResponse,
    MultipleLessonInput,
    VideoInput,
    videoResponse,
    CourseAnalysisResponse,
    CallbackPayload,
)
from app.domain.model.course import Course, Enrollment, Lesson, Video, Payment
from app.repository.courseRepo import CourseRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from app.utils.bunny.bunny import generate_secure_bunny_stream_url, encrypt_secret_key, decrypt_secret_key
from typing import Optional
from app.repository.userRepo import UserRepository
from app.utils.chapa.chapa import pay_course, verify_payment, generete_tx_ref

class CourseService:
    def __init__(self, db):
        self.course_repo = CourseRepository(db)
        self.user_repo = UserRepository(db)
    
    def addCourse(self, course_info: CourseInput):
        # Validate instructor exists and has correct role
        instructor = self.user_repo.get_user_by_id(str(course_info.instructor_id))
        if not instructor or not instructor.role == "instructor":
            raise ValidationError(detail="Invalid instructor ID or not an instructor")
        
        # Create course with instructor relationship
        course_data = course_info.model_dump(exclude={'lessons'})
        course = Course(**course_data)
        
        # Create course first
        created_course = self.course_repo.create_course(course)
        if not created_course:
            raise ValidationError(detail="Failed to create course")
        
        # Add lessons if provided
        if course_info.lessons:
            self.addMultipleLessonsHelper(str(created_course.id), course_info.lessons)


            # lessons = [
            #     Lesson(
            #         **lesson.model_dump(exclude={'video'}),
            #         course_id=created_course.id  # Set course_id here
            #     )
            #     for lesson in course_info.lessons
            # ]
            # self.course_repo.add_multiple_lessons(str(created_course.id), lessons)
        
            # for lesson in course_info.lessons:
            #     video = Video(**lesson.video.model_dump()) if lesson.video else None
                
            #     lesson_data = lesson.model_dump(exclude={'video'})
            #     lesson_instance = Lesson(**lesson_data, video=video)

            #     lessons.append(lesson_instance)
            
            # self.course_repo.add_multiple_lessons(str(created_course.id), lessons)
        
        # Refresh course to get lessons
        created_course = self.course_repo.get_course_with_lessons(str(created_course.id))
        if not created_course:
            raise ValidationError(detail="Failed to fetch course with lessons")
        course_response = CourseResponse.model_validate(created_course)
        # course_response.instructor = UserResponse.model_validate(instructor)
        
        return {
            "detail": "Course created successfully",
            "data": course_response
        }
    
    #get course by using course id
    def getCourse(self, course_id: str):
        # Validate course_id
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        # Get course with lessons
        course = self.course_repo.get_course_with_lessons(course_id)
        if not course:
            raise ValidationError(detail="Course not found")
        
        #TODO remove video from response


        # Convert SQLAlchemy Course object to Pydantic Response Model
        course_response = CourseResponse.model_validate(course)
        
        # Return response
        return {"detail": "course fetched successfully","data": course_response}
    
    #get all courses
    def getCourses(self, page: int = 1, page_size: int = 10, search: Optional[str] = None, filter: Optional[str] = None):
        # Get paginated courses
        courses = self.course_repo.get_courses(page, page_size, search, filter)
        
        # Convert to Pydantic models, excluding lessons
        courses_response = [
            CourseResponse.model_validate(course).model_dump(exclude={'lessons'})
            for course in courses
        ]

        # Return response with pagination metadata
        return {
            "detail": "Courses fetched successfully",
            "data": courses_response,
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
        
        print(user_id)
        # Validate course_id
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        # Validate user exists
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValidationError(detail="User not found")
        

        course = self.course_repo.get_course(course_id)
        if not course:
            raise ValidationError(detail="Course not found")
        
        enrollment = self.course_repo.get_enrollment(user_id, course_id)
        if enrollment:
            raise ValidationError(detail="User already enrolled in course")
        
        if course.price > 0:
            callback = "http://localhost:8000/course/enroll/callback"

            tx_ref = generete_tx_ref(12)
            if course.discount:
                amount = course.price - course.discount * course.price
            else:
                amount = course.price

            data = PaymentData(
                tx_ref=tx_ref,
                user_id=user_id,
                course_id=course_id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                amount=amount,
                title=course.title,
                callback_url=callback
            )
            
            response = pay_course(data)

            if response.get("status") != "success":
                raise ValidationError(detail=response['message'])
            
            payment = Payment(
                user_id=user_id,
                course_id=course_id,
                amount=amount,
                tx_ref=tx_ref
            )
            

            self.course_repo.save_payment(payment)
            
            return {"detail": "Payment initiated", "data": response}
        
        else:
            # Enroll course
            enrollment = self.course_repo.enroll_course(user_id, course_id)
            
            # Convert SQLAlchemy Enrollment object to Pydantic Response Model
            enrollment_response = EnrollmentResponse.model_validate(enrollment)
            
            return {"detail": "Course enrolled successfully", "data": enrollment_response}

    def enrollCourseCallback(self, payload: CallbackPayload):
        # Validate user_id
        print("payload: ",payload)
        payment = self.course_repo.get_payment(payload.trx_ref)
        if not payment:
            raise ValidationError(detail="Payment not found")
        
        response = verify_payment(payload.trx_ref)
        print("verify data",response)
    

        if response["status"] != "success":
            payment = self.course_repo.update_payment(payload.trx_ref, "failed", ref_id=payload.ref_id)
            raise ValidationError(detail="Payment failed")
        
        payment = self.course_repo.update_payment(payload.trx_ref, "success", ref_id=response["data"]["reference"])
        payment = PaymentResponse.model_validate(payment)
        
        # Validate user exists
        user = self.user_repo.get_user_by_id(payment.user_id)
        if not user:
            raise ValidationError(detail="User not found")
        
        # Validate course exists
        course = self.course_repo.get_course(payment.course_id)
        if not course:
            raise ValidationError(detail="Course not found")
        
        # Enroll course
        enrollment = self.course_repo.enroll_course(user.id, course.id)
        
        # Convert SQLAlchemy Enrollment object to Pydantic Response Model
        enrollment_response = EnrollmentResponse.model_validate(enrollment)
        
        return {"detail": "Course enrolled successfully", "data": enrollment_response}
    

    #get all courses enrolled by user
    def getEnrolledCourses(self, user_id: str, page: int = 1, page_size: int = 10, search: Optional[str] = None):
        # Validate user_id
        if not user_id:
            raise ValidationError(detail="User ID is required")
        
        # Get paginated courses
        enrollments = self.course_repo.get_enrolled_courses(user_id, page, page_size, search)
        
        # Extract and convert courses
        courses_response = [
            CourseResponse.model_validate(enrollment.course)
            for enrollment in enrollments
        ]

        # Return response with pagination metadata
        return {
            "detail": "User courses fetched successfully",
            "data": courses_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.course_repo.get_user_courses_count(user_id, search)
            }
        }
    
    #get all users enrolled in a course
    def getEnrolledUsers(self, course_id: str, page: int = 1, page_size: int = 10):
        # Validate course_id
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        # Get paginated users
        users = self.course_repo.get_enrolled_users(course_id, page, page_size)
        
        # Convert to Pydantic models
        users_response = [
            UserResponse.model_validate(user)
            for user in users
        ]

        # Return response with pagination metadata
        return {
            "detail": "Course users fetched successfully",
            "data": users_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.course_repo.get_enrolled_users_count(course_id)
            }
        }
    

    def checkLessonAccess (self,course_id,user_id):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValidationError(detail="User not found")
        
        #check if user is enrolled in course
        enrollment = self.course_repo.get_enrollment(user_id, course_id)
        print(user.role)
        if not enrollment and user.role not in ["instructor", "admin"]:
            raise ValidationError(detail="User not enrolled in course")
        return True
    
    #get all lessons of course
    def getLessons(self, course_id: str,user_id , page: int = 1, page_size: int = 10):
        
        self.checkLessonAccess(course_id,user_id)
        lessons = self.course_repo.get_lessons(course_id, page, page_size)
        lessons_response = [
            LessonResponse.model_validate(lesson)
            for lesson in lessons
        ]
        
        return {
            "detail": "Lessons fetched successfully",
            "data": lessons_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.course_repo.get_lessons_count(course_id)
            }
        }
    
    #get lesson by id
    def getLessonById(self, course_id: str, lesson_id: str, user_id:str):
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        if not lesson_id:
            raise ValidationError(detail="Lesson ID is required")
        
        self.checkLessonAccess(course_id,user_id)

        lesson = self.course_repo.get_lesson_by_id(course_id, lesson_id)
        lesson_response = LessonResponse.model_validate(lesson)

        video = self.course_repo.get_lesson_video(lesson_id)
        if video:
            video_Response = videoResponse.model_validate(video)
            library_id,video_id,secret_key=video_Response.library_id, video_Response.video_id, video_Response.secret_key
            # print(secret_key)
            if  secret_key:
                try:
                    secret_key = decrypt_secret_key(secret_key)
                except Exception as e:
                    raise ValidationError(detail=f"Failed to decrypt video secret key: {str(e)}")
            
            url = generate_secure_bunny_stream_url(library_id, video_id, secret_key)
            lesson_response.video_url = url
        else:
            print("No video found")
        
        return {
            "detail": "Lesson fetched successfully",
            "data": lesson_response
        }
    
    def addMultipleLessonsHelper(self, course_id: str, lessons_input):
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        lessons_responses = []
        for lesson in lessons_input:
            print(lesson)
            lesson_data = Lesson(**lesson.model_dump(exclude={'video'}))
            lesson_data.course_id = course_id

            try:

                created_lesson = self.course_repo.add_lesson(course_id, lesson_data)
            except IntegrityError as e:
                print(f"Error: {str(e)}")
                raise ValidationError(detail=f"Failed to add lesson, {str(e)}")
            
            lesson_response = LessonResponse.model_validate(created_lesson)
            lessons_responses.append(lesson_response)

            if lesson.video:
                self.add_video_to_lesson_helper(course_id, created_lesson.id, lesson.video)
                

        return lessons_responses
    
    def addMultipleLessons(self, course_id: str, lessons_input: MultipleLessonInput):
        return {
            "detail": "Lessons added successfully",
            "data": self.addMultipleLessonsHelper(course_id, lessons_input)
        }

    def add_video_to_lesson_helper(self, course_id: str, lesson_id: str, video_input: VideoInput):
        # Get lesson and check if a available
        lesson = self.course_repo.get_lesson_by_id(course_id,lesson_id)  
        if not lesson:
            raise ValidationError(detail="Lesson not found")

        
        # Create video
        video_input.secret_key = encrypt_secret_key(video_input.secret_key)
        video_data = video_input.model_dump()
        video = Video(**video_data, lesson_id=lesson_id)
        
        # Add video to lesson
        try:
            created_video = self.course_repo.add_video(video)
        except IntegrityError:
            raise ValidationError(detail="Failed to add video, video already exists")
        
        return created_video
        
    def add_video_to_lesson(self, course_id: str, lesson_id: str, video_input: VideoInput):
        
        created_video = self.add_video_to_lesson_helper(course_id, lesson_id, video_input)
        return {
            "detail": "Video added successfully",
            "data": created_video
        }

    def get_lesson_video(self, course_id: str, lesson_id: str):
        # Validate course and lesson exist
        
        video = self.course_repo.get_lesson_video(lesson_id)
        if not video:
            return {
                "detail": "No video found for this lesson",
                "data": None
            }
            
        return {
            "detail": "Video fetched successfully",
            "data": videoResponse.model_validate(video.__dict__)
        }

    def get_video_by_id(self, course_id: str, lesson_id: str, video_id: str):
        # Validate course and lesson exist
        lesson = self.course_repo.get_lesson_by_id(course_id,lesson_id)  
        if not lesson:
            raise ValidationError(detail="Lesson not found")
        
        video = self.course_repo.get_video_by_id(lesson_id, video_id)
        if not video:
            raise ValidationError(detail="Video not found")
        
        return {
            "detail": "Video fetched successfully",
            "data": videoResponse.model_validate(video)
        }

    def get_courses_analysis(self, course_id: str):
        # Validate course_id
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
        # Validate instructor_id
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
        
        
def get_course_service(db: Session = Depends(get_db)):
    return CourseService(db)