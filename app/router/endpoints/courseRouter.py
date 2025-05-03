# from fastapi import APIRouter, Depends
# from app.domain.schema.courseSchema import (
#     CourseInput,
#     SearchParams,
# )
# from app.service.courseService import CourseService, get_course_service
# from app.utils.middleware.dependancies import is_admin, is_logged_in
# from uuid import UUID

# courseRouter = APIRouter(
#     prefix="/course",
#     tags=["course"]
# )

# #get all courses
# @courseRouter.get("/")
# async def get_courses(
#     search_params: SearchParams = Depends(),
#     course_service: CourseService = Depends(get_course_service)
# ):
#     return course_service.getCourses(
#         page=search_params.page,
#         page_size=search_params.page_size,
#         search=search_params.search,
#         filter=search_params.filter
#     )

# #get all courses enrolled by user
# @courseRouter.get("/enrolled")
# async def get_enrolled_courses(
#     search_params: SearchParams = Depends(),
#     decoded_token: dict = Depends(is_logged_in),
#     course_service: CourseService = Depends(get_course_service)
# ):
#     user_id = decoded_token.get("id")
#     user_id = UUID(user_id)
#     response = course_service.getEnrolledCourses(
#         user_id=user_id,
#         page=search_params.page,
#         page_size=search_params.page_size,
#         search=search_params.search
#     )
#     return response

# # Payment endpoints moved to payment_router.py

# #get course by using course id
# @courseRouter.get("/{course_id}")
# async def get_course(
#     course_id: str,
#     course_service: CourseService = Depends(get_course_service)
# ):
#     courseResponse = course_service.getCourse(course_id)
#     return courseResponse

# #enroll course only for logged in user
# @courseRouter.post("/{course_id}/enroll")
# async def enroll_course(
#     course_id: str,
#     decoded_token: dict = Depends(is_logged_in),
#     course_service: CourseService = Depends(get_course_service)
# ):
#     user_id = decoded_token.get("id")

#     user_id = UUID(user_id)
#     course_id = UUID(course_id)

#     enrollResponse = course_service.enrollCourse(user_id, course_id)
#     return enrollResponse

# @courseRouter.get("/{course_id}/enrollment/{user_id}")
# async def get_enrollment(
#     course_id: str,
#     user_id: str,
#     course_service: CourseService = Depends(get_course_service)
# ):
#     user_id = UUID(user_id)
#     course_id = UUID(course_id)
#     return course_service.getEnrollment(user_id, course_id)

# #get all lessons of course
# # Lesson endpoints moved to lesson_router.py

# # Lesson endpoints moved to lesson_router.py


# # Lesson endpoints moved to lesson_router.py

# #create protected router for admin
# protected_courseRouter = APIRouter(
#     prefix="/protected/course",
#     tags=["course"],
#     dependencies=[Depends(is_admin)]
# )

# #add course
# @protected_courseRouter.post("/add")
# async def add_course(
#     course_info: CourseInput,
#     course_service: CourseService = Depends(get_course_service),
#     _: dict = Depends(is_admin)  # Only admins can create courses
# ):
#     return course_service.addCourse(course_info)

# # Payment endpoints moved to payment_router.py

# #get enrolled course of user
# @protected_courseRouter.get("/enrolled/{user_id}")
# async def get_enrolled_courses_by_user(
#     user_id: str,
#     search_params: SearchParams = Depends(),
#     course_service: CourseService = Depends(get_course_service)
# ):
#     return course_service.getEnrolledCourses(
#         user_id=user_id,
#         page=search_params.page,
#         page_size=search_params.page_size,
#         search=search_params.search
#     )

# # Lesson and video endpoints moved to lesson_router.py

# #get all user enrolled course
# @protected_courseRouter.get("/{course_id}/enrolled")
# async def get_all_enrolled_courses(
#     course_id: str,
#     search_params: SearchParams = Depends(),
#     course_service: CourseService = Depends(get_course_service)
# ):
#     return course_service.getEnrolledUsers(
#         course_id,
#         search_params.page,
#         search_params.page_size
#     )

# # Payment endpoints moved to payment_router.py


# analysis_router = APIRouter(
#     prefix="/analysis",
#     tags=["course"]
# )
# # get course of instructor
# @analysis_router.get("/instructor/{instructor_id}")
# async def get_courses_by_instructor(
#     instructor_id: str,
#     course_service: CourseService = Depends(get_course_service)
# ):
#     return course_service.get_intructor_course(
#         instructor_id,
#     )

# # get all courses with analysis
# @analysis_router.get("/{course_id}")
# async def get_courses_analysis(
#     course_id: str,
#     course_service: CourseService = Depends(get_course_service)
# ):
#     return course_service.get_courses_analysis(course_id)
