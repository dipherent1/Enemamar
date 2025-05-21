from sqlalchemy.orm import Session, joinedload
from app.domain.model.course import Comment, Review, Course
from app.utils.exceptions.exceptions import NotFoundError, ValidationError
from typing import Tuple, Optional, Any, List
from sqlalchemy import func, or_
from uuid import UUID

def _wrap_return(result: Any) -> Tuple[Any, None]:
    return result, None
def _wrap_error(e: Exception) -> Tuple[None, Exception]:
    return None, e

class CommentReviewRepository:
    """
    Repository class for handling comment and review-related database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the CommentReviewRepository.

        Args:
            db (Session): The database session.
        """
        self.db = db

    # Comment methods
    def create_comment(self, comment: Comment) -> Comment:
        """
        Create a new comment in the database.

        Args:
            comment (Comment): The comment object to be created.

        Returns:
            Comment: The created comment object.
        """
        try:
            self.db.add(comment)
            self.db.commit()
            self.db.refresh(comment)
            return _wrap_return(comment)
        except Exception as e:
            self.db.rollback()
            return _wrap_error(e)

    def get_comment(self, comment_id: str) -> Comment:
        """
        Get a comment by its ID.

        Args:
            comment_id (str): The ID of the comment.

        Returns:
            Comment: The comment object.

        Raises:
            NotFoundError: If the comment is not found.
        """
        try:
            comment = (self.db.query(Comment)
                .options(joinedload(Comment.user), joinedload(Comment.course))
                .filter(Comment.id == comment_id).first())
            if not comment:
                return None, NotFoundError(detail="Comment not found")
            return _wrap_return(comment)
        except Exception as e:
            return _wrap_error(e)

    def get_comments_by_course(self, course_id: str, page: int = 1, page_size: int = 10) -> List[Comment]:
        """
        Get all comments for a course with pagination.

        Args:
            course_id (str): The ID of the course.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            List[Comment]: A list of comment objects.

        Raises:
            NotFoundError: If the course is not found.
        """
        try:
            course = self.db.query(Course).filter(Course.id == course_id).first()
            if not course:
                return None, NotFoundError(detail="Course not found for comments")
            comments = (self.db.query(Comment).options(joinedload(Comment.user))
                .filter(Comment.course_id == course_id)
                .order_by(Comment.created_at.desc())
                .offset((page - 1) * page_size).limit(page_size).all())
            return _wrap_return(comments)
        except Exception as e:
            return _wrap_error(e)

    def get_comments_by_user(self, user_id: str, page: int = 1, page_size: int = 10) -> Tuple[Optional[List[Comment]], Optional[Exception]]:
        """
        Get all comments by a user with pagination.

        Args:
            user_id (str): The ID of the user.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            Tuple[Optional[List[Comment]], Optional[Exception]]: A list of comment objects or an error.
        """
        try:
            comments = (
                self.db.query(Comment)
                .options(joinedload(Comment.course))
                .filter(Comment.user_id == user_id)
                .order_by(Comment.created_at.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
            return _wrap_return(comments)
        except Exception as e:
            return _wrap_error(e)

    def update_comment(self, comment_id: str, content: str) -> Comment:
        """
        Update a comment.

        Args:
            comment_id (str): The ID of the comment.
            content (str): The new content of the comment.

        Returns:
            Comment: The updated comment object.

        Raises:
            NotFoundError: If the comment is not found.
        """
        try:
            comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                return None, NotFoundError(detail="Comment not found to update")
            comment.content = content
            self.db.commit()
            self.db.refresh(comment)
            return _wrap_return(comment)
        except Exception as e:
            return _wrap_error(e)

    def delete_comment(self, comment_id: str) -> None:
        """
        Delete a comment.

        Args:
            comment_id (str): The ID of the comment.

        Raises:
            NotFoundError: If the comment is not found.
        """
        try:
            comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                return None, NotFoundError(detail="Comment not found to delete")
            self.db.delete(comment)
            self.db.commit()
            return _wrap_return({'deleted': True})
        except Exception as e:
            return _wrap_error(e)

    def get_comments_count_by_course(self, course_id: str) -> Tuple[Optional[int], Optional[Exception]]:
        """
        Get the count of comments for a course.

        Args:
            course_id (str): The ID of the course.

        Returns:
            Tuple[Optional[int], Optional[Exception]]: The number of comments or an error.
        """
        try:
            count = (
                self.db.query(Comment)
                .filter(Comment.course_id == course_id)
                .count()
            )
            return _wrap_return(count)
        except Exception as e:
            return _wrap_error(e)

    def get_comments_count_by_user(self, user_id: str) -> Tuple[Optional[int], Optional[Exception]]:
        """
        Get the count of comments by a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            Tuple[Optional[int], Optional[Exception]]: The number of comments or an error.
        """
        try:
            count = (
                self.db.query(Comment)
                .filter(Comment.user_id == user_id)
                .count()
            )
            return _wrap_return(count)
        except Exception as e:
            return _wrap_error(e)

    # Review methods
    def create_review(self, review: Review) -> Review:
        """
        Create a new review in the database.

        Args:
            review (Review): The review object to be created.

        Returns:
            Review: The created review object.
        """
        try:
            existing_review = (self.db.query(Review)
                .filter(Review.user_id == review.user_id, Review.course_id == review.course_id).first())
            if existing_review:
                return None, ValidationError(detail="Review already exists for user and course")
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)
            return _wrap_return(review)
        except Exception as e:
            return _wrap_error(e)

    def get_review(self, review_id: str) -> Review:
        """
        Get a review by its ID.

        Args:
            review_id (str): The ID of the review.

        Returns:
            Review: The review object.

        Raises:
            NotFoundError: If the review is not found.
        """
        try:
            review = (self.db.query(Review)
                .options(joinedload(Review.user), joinedload(Review.course))
                .filter(Review.id == review_id).first())
            if not review:
                return None, NotFoundError(detail="Review not found")
            return _wrap_return(review)
        except Exception as e:
            return _wrap_error(e)

    def get_reviews_by_course(self, course_id: str, page: int = 1, page_size: int = 10) -> List[Review]:
        """
        Get all reviews for a course with pagination.

        Args:
            course_id (str): The ID of the course.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            List[Review]: A list of review objects.

        Raises:
            NotFoundError: If the course is not found.
        """
        try:
            course = self.db.query(Course).filter(Course.id == course_id).first()
            if not course:
                return None, NotFoundError(detail="Course not found")
            reviews = (self.db.query(Review).options(joinedload(Review.user))
                .filter(Review.course_id == course_id)
                .order_by(Review.created_at.desc())
                .offset((page - 1) * page_size).limit(page_size).all())
            return _wrap_return(reviews)
        except Exception as e:
            return _wrap_error(e)

    def get_reviews_by_user(self, user_id: str, page: int = 1, page_size: int = 10) -> Tuple[Optional[List[Review]], Optional[Exception]]:
        """
        Get all reviews by a user with pagination.

        Args:
            user_id (str): The ID of the user.
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            Tuple[Optional[List[Review]], Optional[Exception]]: A list of review objects or an error.
        """
        try:
            reviews = (
                self.db.query(Review)
                .options(joinedload(Review.course))
                .filter(Review.user_id == user_id)
                .order_by(Review.created_at.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
            return _wrap_return(reviews)
        except Exception as e:
            return _wrap_error(e)

    def update_review(self, review_id: str, rating: int) -> Review:
        """
        Update a review.

        Args:
            review_id (str): The ID of the review.
            rating (int): The new rating of the review.

        Returns:
            Review: The updated review object.

        Raises:
            NotFoundError: If the review is not found.
            ValidationError: If the rating is invalid.
        """
        try:
            if rating < 1 or rating > 5:
                return None, ValidationError(detail="Rating must be between 1 and 5")
            review = self.db.query(Review).filter(Review.id == review_id).first()
            if not review:
                return None, NotFoundError(detail="Review not found to update")
            review.rating = rating
            self.db.commit()
            self.db.refresh(review)
            return _wrap_return(review)
        except Exception as e:
            return _wrap_error(e)

    def delete_review(self, review_id: str) -> None:
        """
        Delete a review.

        Args:
            review_id (str): The ID of the review.

        Raises:
            NotFoundError: If the review is not found.
        """
        try:
            review = self.db.query(Review).filter(Review.id == review_id).first()
            if not review:
                return None, NotFoundError(detail="Review not found to delete")
            self.db.delete(review)
            self.db.commit()
            return _wrap_return({'deleted': True})
        except Exception as e:
            return _wrap_error(e)

    def get_reviews_count_by_course(self, course_id: str) -> Tuple[Optional[int], Optional[Exception]]:
        """
        Get the count of reviews for a course.

        Args:
            course_id (str): The ID of the course.

        Returns:
            Tuple[Optional[int], Optional[Exception]]: The number of reviews or an error.
        """
        try:
            count = (
                self.db.query(Review)
                .filter(Review.course_id == course_id)
                .count()
            )
            return _wrap_return(count)
        except Exception as e:
            return _wrap_error(e)

    def get_reviews_count_by_user(self, user_id: str) -> Tuple[Optional[int], Optional[Exception]]:
        """
        Get the count of reviews by a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            Tuple[Optional[int], Optional[Exception]]: The number of reviews or an error.
        """
        try:
            count = (
                self.db.query(Review)
                .filter(Review.user_id == user_id)
                .count()
            )
            return _wrap_return(count)
        except Exception as e:
            return _wrap_error(e)

    def get_average_rating_by_course(self, course_id: str) -> Tuple[Optional[float], Optional[Exception]]:
        """
        Get the average rating for a course.

        Args:
            course_id (str): The ID of the course.

        Returns:
            Tuple[Optional[float], Optional[Exception]]: The average rating, or 0.0 if there are no reviews, or an error.
        """
        try:
            avg = (
                self.db
                .query(func.avg(Review.rating))
                .filter(Review.course_id == course_id)
                .scalar()
            )
            return _wrap_return(float(avg) if avg is not None else 0.0)
        except Exception as e:
            return _wrap_error(e)

    def get_user_review_for_course(self, user_id: str, course_id: str) -> Tuple[Optional[Review], Optional[Exception]]:
        """
        Get a user's review for a specific course.

        Args:
            user_id (str): The ID of the user.
            course_id (str): The ID of the course.

        Returns:
            Tuple[Optional[Review], Optional[Exception]]: The review object if found, or an error.
        """
        try:
            review = (
                self.db.query(Review)
                .filter(Review.user_id == user_id)
                .filter(Review.course_id == course_id)
                .first()
            )
            return _wrap_return(review)
        except Exception as e:
            return _wrap_error(e)
