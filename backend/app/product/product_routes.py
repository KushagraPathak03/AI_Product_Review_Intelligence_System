from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.common.enums import ProductCategory
from app.product.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.product.product_service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=201,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    return ProductService.create_product(
        db=db,
        product=product,
    )


@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_products(
    keyword: str | None = None,
    brand: str | None = None,
    category: ProductCategory | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
):
    return ProductService.get_products(
        db=db,
        keyword=keyword,
        brand=brand,
        category=category,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    return ProductService.get_product(
        db=db,
        product_id=product_id,
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    return ProductService.update_product(
        db=db,
        product_id=product_id,
        product=product,
    )


@router.delete(
    "/{product_id}",
    response_model=ProductResponse,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    return ProductService.delete_product(
        db=db,
        product_id=product_id,
    )


@router.patch(
    "/{product_id}/restore",
    response_model=ProductResponse,
)
def restore_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    return ProductService.restore_product(
        db=db,
        product_id=product_id,
    )