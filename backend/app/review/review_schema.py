from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.common.enums import (
    ReviewSource,
    SentimentLabel,
)


class ReviewBase(BaseModel):
    source: ReviewSource
    reviewer_name: Optional[str] = None
    rating: Optional[float] = None
    review_title: Optional[str] = None
    review_text: str
    review_date: Optional[str] = None
    review_url: Optional[str] = None


class ReviewCreate(ReviewBase):
    product_id: int


class ReviewUpdate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    product_id: int
    sentiment: SentimentLabel | None = None

    model_config = ConfigDict(
        from_attributes=True
    )