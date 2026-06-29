from dataclasses import dataclass

from app.common.enums import (
    ProductCategory,
    ReviewSource,
)


@dataclass
class ProductDTO:
    """
    Lightweight product returned from a search page.
    """

    product_name: str
    brand: str | None
    category: ProductCategory | None
    product_url: str
    image_url: str | None = None


@dataclass
class ProductDetailDTO:
    """
    Complete product information extracted
    from a product detail page.
    """

    product_name: str

    brand: str | None

    category: ProductCategory | None

    price: float | None

    mrp: float | None

    discount_percentage: float | None

    rating: float | None

    review_count: int | None

    availability: str | None

    description: str | None

    image_url: str | None

    product_url: str


@dataclass
class ReviewDTO:
    """
    Review extracted from an external source.
    """

    source: ReviewSource

    reviewer_name: str | None

    rating: float | None

    review_title: str | None

    review_text: str

    review_date: str | None

    review_url: str | None