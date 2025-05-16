from fastapi import APIRouter, Depends, status
from app.domain.schema.comment_review_schema import (
    CommentInput,
    ReviewInput
)
from app.domain.schema.responseSchema import (
    CommentListResponse, CommentDetailResponse,
    ReviewListResponse, ReviewDetailResponse,
    BaseResponse, ErrorResponse
)
from app.service.comment_review_service import CommentReviewService, get_comment_review_service
from app.utils.middleware.dependancies import is_logged_in
from uuid import UUID
from typing import Dict, Any

# Comment router
comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

@comment_router.post(
    "/course/{course_id}",
    # response_model=CommentDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a comment to a course",
    description="Add a new comment to a specific course.",
    # responses={
    #     201: {
    #         "description": "Comment added successfully",
    #         "model": CommentDetailResponse
    #     },
    #     400: {
    #         "description": "Bad request",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Invalid input data"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def add_comment(
    course_id: str,
    comment_input: CommentInput,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Add a new comment to a specific course.

    This endpoint allows authenticated users to add comments to courses they have access to.

    - **course_id**: UUID of the course to comment on
    - **content**: The text content of the comment

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.add_comment(
        user_id=user_id,
        course_id=course_id,
        comment_input=comment_input
    )

@comment_router.get(
    "/course/{course_id}",
    # response_model=CommentListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get course comments",
    description="Retrieve a paginated list of comments for a specific course.",
    # responses={
    #     200: {
    #         "description": "Comments retrieved successfully",
    #         "model": CommentListResponse
    #     },
    #     404: {
    #         "description": "Course not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def get_course_comments(
    course_id: str,
    page: int = 1,
    page_size: int = 10,
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Retrieve a paginated list of comments for a specific course.

    This endpoint returns all comments associated with the specified course,
    with pagination support.

    - **course_id**: UUID of the course
    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    """
    return comment_review_service.get_course_comments(
        course_id=course_id,
        page=page,
        page_size=page_size
    )

@comment_router.get(
    "/user",
    # response_model=CommentListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user comments",
    description="Retrieve a paginated list of comments by the current user.",
    # responses={
    #     200: {
    #         "description": "Comments retrieved successfully",
    #         "model": CommentListResponse
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     }
    # }
)
async def get_user_comments(
    page: int = 1,
    page_size: int = 10,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Retrieve a paginated list of comments by the current user.

    This endpoint returns all comments made by the authenticated user,
    with pagination support.

    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.get_user_comments(
        user_id=user_id,
        page=page,
        page_size=page_size
    )

@comment_router.get(
    "/{comment_id}",
    # response_model=CommentDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get comment by ID",
    description="Retrieve a specific comment by its ID.",
    # responses={
    #     200: {
    #         "description": "Comment retrieved successfully",
    #         "model": CommentDetailResponse
    #     },
    #     404: {
    #         "description": "Comment not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Comment not found"}
    #             }
    #         }
    #     }
    # }
)
async def get_comment(
    comment_id: str,
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Retrieve a specific comment by its ID.

    This endpoint returns detailed information about a comment.

    - **comment_id**: UUID of the comment to retrieve
    """
    return comment_review_service.get_comment(comment_id)

@comment_router.put(
    "/{comment_id}",
    # response_model=CommentDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Update comment",
    description="Update a specific comment by its ID.",
    # responses={
    #     200: {
    #         "description": "Comment updated successfully",
    #         "model": CommentDetailResponse
    #     },
    #     400: {
    #         "description": "Bad request",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Invalid input data"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     403: {
    #         "description": "Forbidden",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "You can only update your own comments"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Comment not found"}
    #             }
    #         }
    #     }
    # }
)
async def update_comment(
    comment_id: str,
    comment_input: CommentInput,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Update a specific comment by its ID.

    This endpoint allows users to update their own comments.

    - **comment_id**: UUID of the comment to update
    - **content**: The new text content of the comment

    Authentication is required via JWT token in the Authorization header.
    Only the author of the comment can update it.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.update_comment(
        comment_id=comment_id,
        user_id=user_id,
        comment_input=comment_input
    )

@comment_router.delete(
    "/{comment_id}",
    # response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete comment",
    description="Delete a specific comment by its ID.",
    # responses={
    #     200: {
    #         "description": "Comment deleted successfully",
    #         "model": BaseResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Comment deleted successfully"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     403: {
    #         "description": "Forbidden",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "You can only delete your own comments"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Comment not found"}
    #             }
    #         }
    #     }
    # }
)
async def delete_comment(
    comment_id: str,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Delete a specific comment by its ID.

    This endpoint allows users to delete their own comments.

    - **comment_id**: UUID of the comment to delete

    Authentication is required via JWT token in the Authorization header.
    Only the author of the comment can delete it.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.delete_comment(
        comment_id=comment_id,
        user_id=user_id
    )

# Review router
review_router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@review_router.post(
    "/course/{course_id}",
    # response_model=ReviewDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a review to a course",
    description="Add a new review with rating to a specific course.",
    # responses={
    #     201: {
    #         "description": "Review added successfully",
    #         "model": ReviewDetailResponse
    #     },
    #     400: {
    #         "description": "Bad request",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "User has already reviewed this course"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def add_review(
    course_id: str,
    review_input: ReviewInput,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Add a new review with rating to a specific course.

    This endpoint allows authenticated users to add reviews to courses they have access to.
    A user can only add one review per course.

    - **course_id**: UUID of the course to review
    - **rating**: Rating from 1 to 5

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.add_review(
        user_id=user_id,
        course_id=course_id,
        review_input=review_input
    )

@review_router.get(
    "/course/{course_id}",
    # response_model=ReviewListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get course reviews",
    description="Retrieve a paginated list of reviews for a specific course.",
    # responses={
    #     200: {
    #         "description": "Reviews retrieved successfully",
    #         "model": ReviewListResponse
    #     },
    #     404: {
    #         "description": "Course not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def get_course_reviews(
    course_id: str,
    page: int = 1,
    page_size: int = 10,
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Retrieve a paginated list of reviews for a specific course.

    This endpoint returns all reviews associated with the specified course,
    with pagination support.

    - **course_id**: UUID of the course
    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    """
    return comment_review_service.get_course_reviews(
        course_id=course_id,
        page=page,
        page_size=page_size
    )

@review_router.get(
    "/user",
    # response_model=ReviewListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user reviews",
    description="Retrieve a paginated list of reviews by the current user.",
    # responses={
    #     200: {
    #         "description": "Reviews retrieved successfully",
    #         "model": ReviewListResponse
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     }
    # }
)
async def get_user_reviews(
    page: int = 1,
    page_size: int = 10,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Retrieve a paginated list of reviews by the current user.

    This endpoint returns all reviews made by the authenticated user,
    with pagination support.

    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.get_user_reviews(
        user_id=user_id,
        page=page,
        page_size=page_size
    )

@review_router.get(
    "/course/{course_id}/user",
    # response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get user review for course",
    description="Retrieve the current user's review for a specific course.",
    # responses={
    #     200: {
    #         "description": "Review retrieved successfully",
    #         "content": {
    #             "application/json": {
    #                 "example": {
    #                     "detail": "User review retrieved successfully",
    #                     "data": {
    #                         "id": "123e4567-e89b-12d3-a456-426614174000",
    #                         "rating": 5,
    #                         "user_id": "123e4567-e89b-12d3-a456-426614174001",
    #                         "course_id": "123e4567-e89b-12d3-a456-426614174002",
    #                         "created_at": "2023-01-01T12:00:00Z",
    #                         "updated_at": "2023-01-02T12:00:00Z"
    #                     }
    #                 }
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Course not found"}
    #             }
    #         }
    #     }
    # }
)
async def get_user_review_for_course(
    course_id: str,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Retrieve the current user's review for a specific course.

    This endpoint returns the review made by the authenticated user for the specified course,
    or null if the user has not reviewed the course.

    - **course_id**: UUID of the course

    Authentication is required via JWT token in the Authorization header.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.get_user_review_for_course(
        user_id=user_id,
        course_id=course_id
    )

@review_router.get(
    "/{review_id}",
    # response_model=ReviewDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get review by ID",
    description="Retrieve a specific review by its ID.",
    # responses={
    #     200: {
    #         "description": "Review retrieved successfully",
    #         "model": ReviewDetailResponse
    #     },
    #     404: {
    #         "description": "Review not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Review not found"}
    #             }
    #         }
    #     }
    # }
)
async def get_review(
    review_id: str,
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Retrieve a specific review by its ID.

    This endpoint returns detailed information about a review.

    - **review_id**: UUID of the review to retrieve
    """
    return comment_review_service.get_review(review_id)

@review_router.put(
    "/{review_id}",
    # response_model=ReviewDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Update review",
    description="Update a specific review by its ID.",
    # responses={
    #     200: {
    #         "description": "Review updated successfully",
    #         "model": ReviewDetailResponse
    #     },
    #     400: {
    #         "description": "Bad request",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Rating must be between 1 and 5"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     403: {
    #         "description": "Forbidden",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "You can only update your own reviews"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Review not found"}
    #             }
    #         }
    #     }
    # }
)
async def update_review(
    review_id: str,
    review_input: ReviewInput,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Update a specific review by its ID.

    This endpoint allows users to update their own reviews.

    - **review_id**: UUID of the review to update
    - **rating**: The new rating from 1 to 5

    Authentication is required via JWT token in the Authorization header.
    Only the author of the review can update it.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.update_review(
        review_id=review_id,
        user_id=user_id,
        review_input=review_input
    )

@review_router.delete(
    "/{review_id}",
    # response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete review",
    description="Delete a specific review by its ID.",
    # responses={
    #     200: {
    #         "description": "Review deleted successfully",
    #         "model": BaseResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Review deleted successfully"}
    #             }
    #         }
    #     },
    #     401: {
    #         "description": "Unauthorized",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Missing or invalid token"}
    #             }
    #         }
    #     },
    #     403: {
    #         "description": "Forbidden",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "You can only delete your own reviews"}
    #             }
    #         }
    #     },
    #     404: {
    #         "description": "Not found",
    #         "model": ErrorResponse,
    #         "content": {
    #             "application/json": {
    #                 "example": {"detail": "Review not found"}
    #             }
    #         }
    #     }
    # }
)
async def delete_review(
    review_id: str,
    decoded_token: dict = Depends(is_logged_in),
    comment_review_service: CommentReviewService = Depends(get_comment_review_service)
):
    """
    Delete a specific review by its ID.

    This endpoint allows users to delete their own reviews.

    - **review_id**: UUID of the review to delete

    Authentication is required via JWT token in the Authorization header.
    Only the author of the review can delete it.
    """
    user_id = decoded_token.get("id")
    user_id = UUID(user_id)
    return comment_review_service.delete_review(
        review_id=review_id,
        user_id=user_id
    )
