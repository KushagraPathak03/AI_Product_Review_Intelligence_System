from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.base_repository import BaseRepository
from app.common.enums import (
    ReviewSource,
    SentimentLabel,
)

from app.review.review_model import Review
from app.review.review_schema import (
    ReviewCreate,
    ReviewUpdate,
)


class ReviewRepository(BaseRepository[Review]):

    def __init__(self):
        super().__init__(Review)

    def get_by_hash(
        self,
        db: Session,
        review_hash: str,
    ) -> Review | None:
        """
        Get a review by its unique hash.
        """

        return (
            db.query(Review)
            .filter(
                Review.review_hash == review_hash,
            )
            .first()
        )

    def exists_by_hash(
        self,
        db: Session,
        review_hash: str,
    ) -> bool:
        """
        Check whether a review hash already exists.
        """

        return (
            self.get_by_hash(
                db=db,
                review_hash=review_hash,
            )
            is not None
        )

    def create_review(
        self,
        db: Session,
        review: ReviewCreate,
        review_hash: str,
    ) -> Review:
        """
        Create a new review.
        """

        db_review = Review(
            product_id=review.product_id,
            source=review.source,
            reviewer_name=review.reviewer_name,
            rating=review.rating,
            review_title=review.review_title,
            review_text=review.review_text,
            review_date=review.review_date,
            review_url=review.review_url,
            review_hash=review_hash,
        )

        return self.create(
            db=db,
            obj=db_review,
        )

    def update_review(
        self,
        db: Session,
        db_review: Review,
        review: ReviewUpdate,
        review_hash: str,
    ) -> Review:
        """
        Update an existing review.
        """

        db_review.source = review.source
        db_review.reviewer_name = review.reviewer_name
        db_review.rating = review.rating
        db_review.review_title = review.review_title
        db_review.review_text = review.review_text
        db_review.review_date = review.review_date
        db_review.review_url = review.review_url
        db_review.review_hash = review_hash

        return self.update(
            db=db,
            obj=db_review,
        )

    def get_reviews_by_product(
        self,
        db: Session,
        product_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Review]:

        return (
            db.query(Review)
            .filter(
                Review.product_id == product_id,
            )
            .order_by(
                Review.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_reviews(
        self,
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Review]:

        return (
            db.query(Review)
            .filter(
                Review.review_text.ilike(f"%{keyword}%"),
            )
            .order_by(
                Review.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def filter_reviews(
        self,
        db: Session,
        source: ReviewSource | None = None,
        sentiment: SentimentLabel | None = None,
        rating: float | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Review]:

        query = db.query(Review)

        if source:
            query = query.filter(
                Review.source == source,
            )

        if sentiment:
            query = query.filter(
                Review.sentiment == sentiment,
            )

        if rating is not None:
            query = query.filter(
                Review.rating == rating,
            )

        return (
            query
            .order_by(
                Review.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_average_rating(
        self,
        db: Session,
        product_id: int,
    ) -> float:
        """
        Get the average rating for a product.
        """

        rating = (
            db.query(
                func.avg(
                    Review.rating,
                )
            )
            .filter(
                Review.product_id == product_id,
            )
            .scalar()
        )

        return rating or 0.0

    def get_review_count(
        self,
        db: Session,
        product_id: int,
    ) -> int:
        """
        Get the total number of reviews for a product.
        """

        return (
            db.query(Review)
            .filter(
                Review.product_id == product_id,
            )
            .count()
        )


review_repository = ReviewRepository()