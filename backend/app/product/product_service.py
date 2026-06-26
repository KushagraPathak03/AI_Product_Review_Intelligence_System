from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.enums import ProductCategory
from app.common.utils import normalize_product_name
from app.product.product_repository import product_repository
from app.product.product_schema import (
    ProductCreate,
    ProductUpdate,
)


class ProductService:

    @staticmethod
    def create_product(
        db: Session,
        product: ProductCreate,
    ):
        """
        Create a new product after checking for duplicates.
        """

        normalized_name = normalize_product_name(
            product.product_name
        )

        existing_product = (
            product_repository.get_by_normalized_name(
                db=db,
                normalized_name=normalized_name,
            )
        )

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product '{product.product_name}' already exists.",
            )

        return product_repository.create_product(
            db=db,
            product=product,
            normalized_name=normalized_name,
        )

    @staticmethod
    def get_products(
        db: Session,
        keyword: str | None = None,
        brand: str | None = None,
        category: ProductCategory | None = None,
        page: int = 1,
        page_size: int = 20,
    ):
        """
        Get products with optional search, filtering and pagination.
        """

        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page must be greater than 0.",
            )

        if page_size < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page size must be greater than 0.",
            )

        skip = (page - 1) * page_size

        return product_repository.get_products(
            db=db,
            keyword=keyword,
            brand=brand,
            category=category,
            skip=skip,
            limit=page_size,
        )

    @staticmethod
    def get_product(
        db: Session,
        product_id: int,
    ):
        """
        Return a product by ID.
        """

        product = product_repository.get_by_id(
            db=db,
            obj_id=product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return product

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product: ProductUpdate,
    ):
        """
        Update an existing product.
        """

        db_product = product_repository.get_by_id(
            db=db,
            obj_id=product_id,
        )

        if db_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        normalized_name = normalize_product_name(
            product.product_name
        )

        existing_product = (
            product_repository.get_by_normalized_name(
                db=db,
                normalized_name=normalized_name,
            )
        )

        if (
            existing_product
            and existing_product.id != product_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another product with the same name already exists.",
            )

        return product_repository.update_product(
            db=db,
            db_product=db_product,
            product=product,
            normalized_name=normalized_name,
        )

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ):
        """
        Soft delete a product.
        """

        product = product_repository.get_by_id(
            db=db,
            obj_id=product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return product_repository.soft_delete(
            db=db,
            product=product,
        )

    @staticmethod
    def restore_product(
        db: Session,
        product_id: int,
    ):
        """
        Restore a soft-deleted product.
        """

        product = product_repository.get_by_id(
            db=db,
            obj_id=product_id,
            include_deleted=True,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return product_repository.restore_product(
            db=db,
            product=product,
        )