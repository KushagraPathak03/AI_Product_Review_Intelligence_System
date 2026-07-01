from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.common.enums import ProductCategory


class ProductBase(BaseModel):
    """
    Base schema for Product.
    """

    product_name: str

    brand: str

    category: ProductCategory

    model_number: Optional[str] = None

    launch_year: Optional[int] = None

    image_url: Optional[str] = None

    price: Optional[float] = None

    mrp: Optional[float] = None

    discount_percentage: Optional[float] = None

    rating: Optional[float] = None

    review_count: Optional[int] = None

    availability: Optional[str] = None

    description: Optional[str] = None

    product_url: Optional[str] = None


class ProductCreate(ProductBase):
    """
    Schema used when creating a product.
    """
    pass


class ProductUpdate(ProductBase):
    """
    Schema used when updating a product.
    """
    pass


class ProductResponse(ProductBase):
    """
    Product response schema.
    """

    id: int

    is_deleted: bool

    model_config = ConfigDict(
        from_attributes=True
    )