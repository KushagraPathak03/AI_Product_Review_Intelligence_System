from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.common.enums import (
    ReviewSource,
    SentimentLabel,
)

from app.review.review_schema import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
)

from app.review.review_service import ReviewService


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=201,
)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
):
    return ReviewService.create_review(
        db=db,
        review=review,
    )


@router.get(
    "",
    response_model=list[ReviewResponse],
)
def get_reviews(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return ReviewService.get_reviews(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    return ReviewService.get_review(
        db=db,
        review_id=review_id,
    )


@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
)
def update_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
):
    return ReviewService.update_review(
        db=db,
        review_id=review_id,
        review=review,
    )


@router.delete(
    "/{review_id}",
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    return ReviewService.delete_review(
        db=db,
        review_id=review_id,
    )


@router.get(
    "/product/{product_id}",
    response_model=list[ReviewResponse],
)
def get_reviews_by_product(
    product_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return ReviewService.get_reviews_by_product(
        db=db,
        product_id=product_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/search/",
    response_model=list[ReviewResponse],
)
def search_reviews(
    keyword: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return ReviewService.search_reviews(
        db=db,
        keyword=keyword,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/filter/",
    response_model=list[ReviewResponse],
)
def filter_reviews(
    source: ReviewSource | None = None,
    sentiment: SentimentLabel | None = None,
    rating: float | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return ReviewService.filter_reviews(
        db=db,
        source=source,
        sentiment=sentiment,
        rating=rating,
        skip=skip,
        limit=limit,
    )