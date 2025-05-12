from app.utils.exceptions.exceptions import ValidationError, NotFoundError
from app.domain.schema.comment_review_schema import (
    CommentInput,
    CommentResponse,
    ReviewInput,
    ReviewResponse,
    CourseCommentResponse,
    CourseReviewResponse
)
from app.domain.model.course import Comment, Review
from app.repository.comment_review_repo import CommentReviewRepository
from app.repository.courseRepo import CourseRepository
from app.repository.userRepo import UserRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from typing import Optional, List
from uuid import UUID

class CommentReviewService:
    def __init__(self, db):
        """
        Initialize the CommentReviewService with the database session and repositories.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db
        self.comment_review_repo = CommentReviewRepository(db)
        self.course_repo = CourseRepository(db)
        self.user_repo = UserRepository(db)

    # Comment methods
    def add_comment(self, user_id: UUID, course_id: str, comment_input: CommentInput):
        """
        Add a new comment to a course.

        Args:
            user_id (UUID): ID of the user adding the comment.
            course_id (str): ID of the course to comment on.
            comment_input (CommentInput): Input data for creating a comment.

        Returns:
            dict: Response containing comment creation details and data.

        Raises:
            ValidationError: If the user or course is invalid or comment creation fails.
        """
        # Validate user
        user = self.user_repo.get_user_by_id(str(user_id))
        if not user:
            raise ValidationError(detail="User not found")

        # Validate course
        try:
            course = self.course_repo.get_course(course_id)
        except NotFoundError:
            raise ValidationError(detail="Course not found")

        # Create comment
        comment = Comment(
            content=comment_input.content,
            user_id=user_id,
            course_id=course_id
        )

        try:
            created_comment = self.comment_review_repo.create_comment(comment)
            comment_response = CommentResponse.model_validate(created_comment)
            return {
                "detail": "Comment added successfully",
                "data": comment_response
            }
        except Exception as e:
            raise ValidationError(detail=f"Failed to add comment: {str(e)}")

    def get_comment(self, comment_id: str):
        """
        Retrieve a comment by its ID.

        Args:
            comment_id (str): ID of the comment to retrieve.

        Returns:
            dict: Response containing comment details.

        Raises:
            ValidationError: If the comment ID is invalid or the comment is not found.
        """
        if not comment_id:
            raise ValidationError(detail="Comment ID is required")

        try:
            comment = self.comment_review_repo.get_comment(comment_id)
            comment_response = CommentResponse.model_validate(comment)
            return {
                "detail": "Comment retrieved successfully",
                "data": comment_response
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    def get_course_comments(self, course_id: str, page: int = 1, page_size: int = 10):
        """
        Retrieve comments for a specific course.

        Args:
            course_id (str): ID of the course.
            page (int): Page number for pagination.
            page_size (int): Number of items per page.

        Returns:
            dict: Response containing paginated comments data and metadata.

        Raises:
            ValidationError: If the course ID is invalid or the course is not found.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        try:
            comments = self.comment_review_repo.get_comments_by_course(course_id, page, page_size)
            comments_response = [CommentResponse.model_validate(comment) for comment in comments]

            return {
                "detail": "Course comments retrieved successfully",
                "data": {
                    "comments": comments_response,
                    "page": page,
                    "page_size": page_size,
                    "total_items": self.comment_review_repo.get_comments_count_by_course(course_id)
                }
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    def get_user_comments(self, user_id: UUID, page: int = 1, page_size: int = 10):
        """
        Retrieve comments by a specific user.

        Args:
            user_id (UUID): ID of the user.
            page (int): Page number for pagination.
            page_size (int): Number of items per page.

        Returns:
            dict: Response containing paginated comments data and metadata.

        Raises:
            ValidationError: If the user ID is invalid or the user is not found.
        """
        if not user_id:
            raise ValidationError(detail="User ID is required")

        # Validate user
        user = self.user_repo.get_user_by_id(str(user_id))
        if not user:
            raise ValidationError(detail="User not found")

        comments = self.comment_review_repo.get_comments_by_user(str(user_id), page, page_size)
        comments_response = [CommentResponse.model_validate(comment) for comment in comments]

        return {
            "detail": "User comments retrieved successfully",
            "data": {
                "comments": comments_response,
                "page": page,
                "page_size": page_size,
                "total_items": self.comment_review_repo.get_comments_count_by_user(str(user_id))
            }
        }

    def update_comment(self, comment_id: str, user_id: UUID, comment_input: CommentInput):
        """
        Update a comment.

        Args:
            comment_id (str): ID of the comment to update.
            user_id (UUID): ID of the user updating the comment.
            comment_input (CommentInput): Input data for updating the comment.

        Returns:
            dict: Response containing updated comment details.

        Raises:
            ValidationError: If the comment ID is invalid, the comment is not found,
                            or the user is not the author of the comment.
        """
        if not comment_id:
            raise ValidationError(detail="Comment ID is required")

        try:
            # Get the comment to check ownership
            comment = self.comment_review_repo.get_comment(comment_id)

            # Check if the user is the author of the comment
            if str(comment.user_id) != str(user_id):
                raise ValidationError(detail="You can only update your own comments")

            # Update the comment
            updated_comment = self.comment_review_repo.update_comment(comment_id, comment_input.content)
            comment_response = CommentResponse.model_validate(updated_comment)

            return {
                "detail": "Comment updated successfully",
                "data": comment_response
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    def delete_comment(self, comment_id: str, user_id: UUID):
        """
        Delete a comment.

        Args:
            comment_id (str): ID of the comment to delete.
            user_id (UUID): ID of the user deleting the comment.

        Returns:
            dict: Response indicating successful deletion.

        Raises:
            ValidationError: If the comment ID is invalid, the comment is not found,
                            or the user is not the author of the comment.
        """
        if not comment_id:
            raise ValidationError(detail="Comment ID is required")

        try:
            # Get the comment to check ownership
            comment = self.comment_review_repo.get_comment(comment_id)

            # Check if the user is the author of the comment
            if str(comment.user_id) != str(user_id):
                raise ValidationError(detail="You can only delete your own comments")

            # Delete the comment
            self.comment_review_repo.delete_comment(comment_id)

            return {
                "detail": "Comment deleted successfully"
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    # Review methods
    def add_review(self, user_id: UUID, course_id: str, review_input: ReviewInput):
        """
        Add a new review to a course.

        Args:
            user_id (UUID): ID of the user adding the review.
            course_id (str): ID of the course to review.
            review_input (ReviewInput): Input data for creating a review.

        Returns:
            dict: Response containing review creation details and data.

        Raises:
            ValidationError: If the user or course is invalid, the user has already reviewed the course,
                            or review creation fails.
        """
        # Validate user
        user = self.user_repo.get_user_by_id(str(user_id))
        if not user:
            raise ValidationError(detail="User not found")

        # Validate course
        try:
            course = self.course_repo.get_course(course_id)
        except NotFoundError:
            raise ValidationError(detail="Course not found")

        # Validate rating
        if review_input.rating < 1 or review_input.rating > 5:
            raise ValidationError(detail="Rating must be between 1 and 5")

        # Create review
        review = Review(
            rating=review_input.rating,
            user_id=user_id,
            course_id=course_id
        )

        try:
            created_review = self.comment_review_repo.create_review(review)
            review_response = ReviewResponse.model_validate(created_review)
            return {
                "detail": "Review added successfully",
                "data": review_response
            }
        except ValidationError as e:
            raise ValidationError(detail=str(e))
        except Exception as e:
            raise ValidationError(detail=f"Failed to add review: {str(e)}")

    def get_review(self, review_id: str):
        """
        Retrieve a review by its ID.

        Args:
            review_id (str): ID of the review to retrieve.

        Returns:
            dict: Response containing review details.

        Raises:
            ValidationError: If the review ID is invalid or the review is not found.
        """
        if not review_id:
            raise ValidationError(detail="Review ID is required")

        try:
            review = self.comment_review_repo.get_review(review_id)
            review_response = ReviewResponse.model_validate(review)
            return {
                "detail": "Review retrieved successfully",
                "data": review_response
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    def get_course_reviews(self, course_id: str, page: int = 1, page_size: int = 10):
        """
        Retrieve reviews for a specific course.

        Args:
            course_id (str): ID of the course.
            page (int): Page number for pagination.
            page_size (int): Number of items per page.

        Returns:
            dict: Response containing paginated reviews data and metadata.

        Raises:
            ValidationError: If the course ID is invalid or the course is not found.
        """
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        try:
            reviews = self.comment_review_repo.get_reviews_by_course(course_id, page, page_size)
            reviews_response = [ReviewResponse.model_validate(review) for review in reviews]
            average_rating = self.comment_review_repo.get_average_rating_by_course(course_id)

            return {
                "detail": "Course reviews retrieved successfully",
                "data": {
                    "reviews": reviews_response,
                    "average_rating": average_rating,
                    "page": page,
                    "page_size": page_size,
                    "total_items": self.comment_review_repo.get_reviews_count_by_course(course_id)
                }
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    def get_user_reviews(self, user_id: UUID, page: int = 1, page_size: int = 10):
        """
        Retrieve reviews by a specific user.

        Args:
            user_id (UUID): ID of the user.
            page (int): Page number for pagination.
            page_size (int): Number of items per page.

        Returns:
            dict: Response containing paginated reviews data and metadata.

        Raises:
            ValidationError: If the user ID is invalid or the user is not found.
        """
        if not user_id:
            raise ValidationError(detail="User ID is required")

        # Validate user
        user = self.user_repo.get_user_by_id(str(user_id))
        if not user:
            raise ValidationError(detail="User not found")

        reviews = self.comment_review_repo.get_reviews_by_user(str(user_id), page, page_size)
        reviews_response = [ReviewResponse.model_validate(review) for review in reviews]

        return {
            "detail": "User reviews retrieved successfully",
            "data": {
                "reviews": reviews_response,
                "page": page,
                "page_size": page_size,
                "total_items": self.comment_review_repo.get_reviews_count_by_user(str(user_id))
            }
        }

    def update_review(self, review_id: str, user_id: UUID, review_input: ReviewInput):
        """
        Update a review.

        Args:
            review_id (str): ID of the review to update.
            user_id (UUID): ID of the user updating the review.
            review_input (ReviewInput): Input data for updating the review.

        Returns:
            dict: Response containing updated review details.

        Raises:
            ValidationError: If the review ID is invalid, the review is not found,
                            or the user is not the author of the review.
        """
        if not review_id:
            raise ValidationError(detail="Review ID is required")

        # Validate rating
        if review_input.rating < 1 or review_input.rating > 5:
            raise ValidationError(detail="Rating must be between 1 and 5")

        try:
            # Get the review to check ownership
            review = self.comment_review_repo.get_review(review_id)

            # Check if the user is the author of the review
            if str(review.user_id) != str(user_id):
                raise ValidationError(detail="You can only update your own reviews")

            # Update the review
            updated_review = self.comment_review_repo.update_review(review_id, review_input.rating)
            review_response = ReviewResponse.model_validate(updated_review)

            return {
                "detail": "Review updated successfully",
                "data": review_response
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    def delete_review(self, review_id: str, user_id: UUID):
        """
        Delete a review.

        Args:
            review_id (str): ID of the review to delete.
            user_id (UUID): ID of the user deleting the review.

        Returns:
            dict: Response indicating successful deletion.

        Raises:
            ValidationError: If the review ID is invalid, the review is not found,
                            or the user is not the author of the review.
        """
        if not review_id:
            raise ValidationError(detail="Review ID is required")

        try:
            # Get the review to check ownership
            review = self.comment_review_repo.get_review(review_id)

            # Check if the user is the author of the review
            if str(review.user_id) != str(user_id):
                raise ValidationError(detail="You can only delete your own reviews")

            # Delete the review
            self.comment_review_repo.delete_review(review_id)

            return {
                "detail": "Review deleted successfully"
            }
        except NotFoundError as e:
            raise ValidationError(detail=str(e))

    def get_user_review_for_course(self, user_id: UUID, course_id: str):
        """
        Get a user's review for a specific course.

        Args:
            user_id (UUID): ID of the user.
            course_id (str): ID of the course.

        Returns:
            dict: Response containing the user's review for the course, or None if not found.

        Raises:
            ValidationError: If the user or course ID is invalid.
        """
        if not user_id:
            raise ValidationError(detail="User ID is required")
        if not course_id:
            raise ValidationError(detail="Course ID is required")

        # Validate user
        user = self.user_repo.get_user_by_id(str(user_id))
        if not user:
            raise ValidationError(detail="User not found")

        # Validate course
        try:
            course = self.course_repo.get_course(course_id)
        except NotFoundError:
            raise ValidationError(detail="Course not found")

        review = self.comment_review_repo.get_user_review_for_course(str(user_id), course_id)
        if not review:
            return {
                "detail": "User has not reviewed this course",
                "data": None
            }

        review_response = ReviewResponse.model_validate(review)
        return {
            "detail": "User review retrieved successfully",
            "data": review_response
        }


def get_comment_review_service(db: Session = Depends(get_db)):
    return CommentReviewService(db)
