from app.utils.exceptions.exceptions import ValidationError
from app.domain.schema.courseSchema import (
    PaymentData,
    PaymentResponse,
    CallbackPayload,
)
from app.domain.model.course import Payment
from app.repository.payment_repo import PaymentRepository
from app.repository.courseRepo import CourseRepository
from app.repository.userRepo import UserRepository
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from typing import Optional
from app.utils.chapa.chapa import pay_course, verify_payment, generete_tx_ref
from app.domain.schema.courseSchema import EnrollmentResponse

class PaymentService:
    def __init__(self, db: Session):
        self.payment_repo = PaymentRepository(db)
        self.course_repo = CourseRepository(db)
        self.user_repo = UserRepository(db)
    
    def initiate_payment(self, user_id, course_id):
        """
        Initiate a payment for a course.
        
        Args:
            user_id: The user ID.
            course_id: The course ID.
            
        Returns:
            dict: The payment response.
            
        Raises:
            ValidationError: If the payment fails.
        """
        # Validate user exists
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValidationError(detail="User not found")
        
        # Validate course exists
        course = self.course_repo.get_course(course_id)
        if not course:
            raise ValidationError(detail="Course not found")
        
        # Check if user is already enrolled
        enrollment = self.course_repo.get_enrollment(user_id, course_id)
        if enrollment:
            raise ValidationError(detail="User already enrolled in course")
        
        if course.price > 0:
            callback = "http://localhost:8000/payment/callback"

            tx_ref = generete_tx_ref(12)
            if course.discount:
                amount = course.price - course.discount * course.price
            else:
                amount = course.price

            data = PaymentData(
                tx_ref=tx_ref,
                user_id=user_id,
                course_id=course_id,
                first_name=user.first_name,
                last_name=user.last_name,
                amount=amount,
                title=course.title,
                callback_url=callback,
                phone_number="0"+user.phone_number
            )
            if user.email:
                data.email = user.email
            try:
                response = pay_course(data)
            except Exception as e:
                raise ValidationError(detail="Payment initiation failed")

            if response.get("status") != "success":
                raise ValidationError(detail=response['message'])
            
            payment = Payment(
                user_id=user_id,
                course_id=course_id,
                amount=amount,
                tx_ref=tx_ref
            )
            
            payment = self.payment_repo.save_payment(payment)
            
            return {"detail": "Payment initiated", "data": {"payment": PaymentResponse.model_validate(payment), "chapa_response": response}}
        
        else:
            # Enroll course for free
            enrollment = self.course_repo.enroll_course(user_id, course_id)
            
            # Convert SQLAlchemy Enrollment object to Pydantic Response Model
            enrollment_response = EnrollmentResponse.model_validate(enrollment)
            
            return {"detail": "Course enrolled successfully", "data": enrollment_response}
    
    def process_payment_callback(self, payload: CallbackPayload):
        """
        Process a payment callback.
        
        Args:
            payload (CallbackPayload): The callback payload.
            
        Returns:
            dict: The enrollment response.
            
        Raises:
            ValidationError: If the payment fails.
        """
        # Validate payment exists
        payment = self.payment_repo.get_payment(payload.trx_ref)
        if not payment:
            raise ValidationError(detail="Payment not found")
        
        # Verify payment with payment provider
        try:
            response = verify_payment(payload.trx_ref)
        except Exception as e:
            raise ValidationError(detail="Payment verification failed")
        
        if response["status"] != "success":
            payment = self.payment_repo.update_payment(payload.trx_ref, "failed", ref_id=payload.ref_id)
            raise ValidationError(detail="Payment failed")
        
        # Update payment status
        payment = self.payment_repo.update_payment(payload.trx_ref, "success", ref_id=response["data"]["reference"])
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
    
    def get_user_payments(self, user_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        """
        Get all payments for a user.
        
        Args:
            user_id (str): The user ID.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The page size. Defaults to 10.
            filter (Optional[str], optional): Filter by payment status. Defaults to None.
            
        Returns:
            dict: The payments response.
            
        Raises:
            ValidationError: If the user is not found.
        """
        # Validate user_id
        if not user_id:
            raise ValidationError(detail="User ID is required")
        
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValidationError(detail="User not found")
        
        # Get paginated payments
        payments = self.payment_repo.get_user_payments(user_id, page, page_size, filter)
        
        # Convert to Pydantic models
        payments_response = [
            PaymentResponse.model_validate(payment)
            for payment in payments
        ]

        # Return response with pagination metadata
        return {
            "detail": "User payments fetched successfully",
            "data": payments_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.payment_repo.get_user_payments_count(user_id, filter)
            }
        }
    
    def get_course_payments(self, course_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        """
        Get all payments for a course.
        
        Args:
            course_id (str): The course ID.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The page size. Defaults to 10.
            filter (Optional[str], optional): Filter by payment status. Defaults to None.
            
        Returns:
            dict: The payments response.
            
        Raises:
            ValidationError: If the course is not found.
        """
        # Validate course_id
        if not course_id:
            raise ValidationError(detail="Course ID is required")
        
        course = self.course_repo.get_course(course_id)
        if not course:
            raise ValidationError(detail="Course not found")
        
        # Get paginated payments
        payments = self.payment_repo.get_course_payments(course_id, page, page_size, filter)
        
        # Convert to Pydantic models
        payments_response = [
            PaymentResponse.model_validate(payment)
            for payment in payments
        ]

        # Return response with pagination metadata
        return {
            "detail": "Course payments fetched successfully",
            "data": payments_response,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": self.payment_repo.get_course_payments_count(course_id, filter)
            }
        }

def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    """
    Get a PaymentService instance.
    
    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        
    Returns:
        PaymentService: A PaymentService instance.
    """
    return PaymentService(db)
