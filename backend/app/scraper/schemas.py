from dataclasses import dataclass


@dataclass
class ProductDTO:
    product_name: str
    brand: str | None
    category: str | None
    product_url: str
    image_url: str | None = None


@dataclass
class ReviewDTO:
    source: str
    reviewer_name: str | None
    rating: float | None
    review_title: str | None
    review_text: str
    review_date: str | None
    review_url: str | None