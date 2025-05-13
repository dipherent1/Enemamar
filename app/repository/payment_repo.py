from sqlalchemy.orm import Session
from app.domain.model.course import Payment
from app.utils.exceptions.exceptions import NotFoundError
from sqlalchemy import func
from typing import Optional

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def save_payment(self, payment: Payment):
        """
        Save a new payment to the database.
        
        Args:
            payment (Payment): The payment object to save.
            
        Returns:
            Payment: The saved payment object.
        """
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
    
    def get_payment(self, tx_ref: str):
        """
        Get a payment by transaction reference.
        
        Args:
            tx_ref (str): The transaction reference.
            
        Returns:
            Payment: The payment object if found, None otherwise.
        """
        payment = (
            self.db.query(Payment)
            .filter(Payment.tx_ref == tx_ref)
            .first()
        )
        return payment
    
    def update_payment(self, tx_ref: str, status: str, ref_id: str):
        """
        Update a payment's status and reference ID.
        
        Args:
            tx_ref (str): The transaction reference.
            status (str): The new status.
            ref_id (str): The reference ID.
            
        Returns:
            Payment: The updated payment object.
            
        Raises:
            NotFoundError: If the payment is not found.
        """
        payment = self.get_payment(tx_ref)
        if not payment:
            raise NotFoundError(detail="Payment not found")
        
        payment.status = status
        payment.ref_id = ref_id
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_user_payments(self, user_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        """
        Get all payments for a user with pagination and optional filtering.
        
        Args:
            user_id (str): The user ID.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The page size. Defaults to 10.
            filter (Optional[str], optional): Filter by payment status. Defaults to None.
            
        Returns:
            List[Payment]: A list of payment objects.
        """
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
    
    def get_course_payments(self, course_id: str, page: int = 1, page_size: int = 10, filter: Optional[str] = None):
        """
        Get all payments for a course with pagination and optional filtering.
        
        Args:
            course_id (str): The course ID.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The page size. Defaults to 10.
            filter (Optional[str], optional): Filter by payment status. Defaults to None.
            
        Returns:
            List[Payment]: A list of payment objects.
        """
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

    def get_user_payments_count(self, user_id: str, filter: Optional[str] = None):
        """
        Get the count of payments for a user with optional filtering.
        
        Args:
            user_id (str): The user ID.
            filter (Optional[str], optional): Filter by payment status. Defaults to None.
            
        Returns:
            int: The count of payments.
        """
        query = self.db.query(Payment).filter(Payment.user_id == user_id)
        if filter is not None:
            query = query.filter(Payment.status == filter)
        return query.count()

    def get_course_payments_count(self, course_id: str, filter: Optional[str] = None):
        """
        Get the count of payments for a course with optional filtering.
        
        Args:
            course_id (str): The course ID.
            filter (Optional[str], optional): Filter by payment status. Defaults to None.
            
        Returns:
            int: The count of payments.
        """
        query = self.db.query(Payment).filter(Payment.course_id == course_id)
        if filter is not None:
            query = query.filter(Payment.status == filter)
        return query.count()

    def get_course_revenue(self, course_id: str):
        """
        Get the total revenue for a course.
        
        Args:
            course_id (str): The course ID.
            
        Returns:
            float: The total revenue.
        """
        total_revenue = (
            self.db.query(func.sum(Payment.amount))
            .filter(Payment.course_id == course_id)
            .filter(Payment.status == "success")
            .scalar()
        )
        return total_revenue or 0.0
