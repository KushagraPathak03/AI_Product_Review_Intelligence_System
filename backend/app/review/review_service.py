from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.hash_utils import generate_review_hash

from app.product.product_repository import product_repository

from app.review.review_repository import review_repository
from app.review.review_schema import (
    ReviewCreate,
    ReviewUpdate,
)


class ReviewService:

    @staticmethod
    def create_review(
        db: Session,
        review: ReviewCreate,
    ):
        """
        Create a review for an existing product.
        """

        product = product_repository.get_by_id(
            db=db,
            obj_id=review.product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        review_hash = generate_review_hash(
            product_id=review.product_id,
            reviewer_name=review.reviewer_name,
            review_title=review.review_title,
            review_text=review.review_text,
        )

        if review_repository.exists_by_hash(
            db=db,
            review_hash=review_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Review already exists.",
            )

        return review_repository.create_review(
            db=db,
            review=review,
            review_hash=review_hash,
        )

    @staticmethod
    def get_reviews(
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ):
        return review_repository.get_all(
            db=db,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def get_review(
        db: Session,
        review_id: int,
    ):

        review = review_repository.get_by_id(
            db=db,
            obj_id=review_id,
        )

        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found.",
            )

        return review

    @staticmethod
    def update_review(
        db: Session,
        review_id: int,
        review: ReviewUpdate,
    ):

        db_review = review_repository.get_by_id(
            db=db,
            obj_id=review_id,
        )

        if db_review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found.",
            )

        review_hash = generate_review_hash(
            product_id=db_review.product_id,
            reviewer_name=review.reviewer_name,
            review_title=review.review_title,
            review_text=review.review_text,
        )

        existing_review = review_repository.get_by_hash(
            db=db,
            review_hash=review_hash,
        )

        if (
            existing_review
            and existing_review.id != review_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another identical review already exists.",
            )

        return review_repository.update_review(
            db=db,
            db_review=db_review,
            review=review,
            review_hash=review_hash,
        )

    @staticmethod
    def delete_review(
        db: Session,
        review_id: int,
    ):

        review = review_repository.get_by_id(
            db=db,
            obj_id=review_id,
        )

        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found.",
            )

        review_repository.delete(
            db=db,
            obj=review,
        )

        return {
            "message": "Review deleted successfully."
        }

    @staticmethod
    def get_reviews_by_product(
        db: Session,
        product_id: int,
        skip: int = 0,
        limit: int = 20,
    ):

        return review_repository.get_reviews_by_product(
            db=db,
            product_id=product_id,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def search_reviews(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return review_repository.search_reviews(
            db=db,
            keyword=keyword,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def filter_reviews(
        db: Session,
        source=None,
        sentiment=None,
        rating=None,
        skip: int = 0,
        limit: int = 20,
    ):

        return review_repository.filter_reviews(
            db=db,
            source=source,
            sentiment=sentiment,
            rating=rating,
            skip=skip,
            limit=limit,
        )