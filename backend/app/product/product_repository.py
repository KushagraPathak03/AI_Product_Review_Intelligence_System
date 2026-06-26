from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.common.enums import ProductCategory
from app.common.base_repository import BaseRepository
from app.product.product_model import Product
from app.product.product_schema import (
    ProductCreate,
    ProductUpdate,
)


class ProductRepository(BaseRepository[Product]):

    def __init__(self):
        super().__init__(Product)

    def create_product(
        self,
        db: Session,
        product: ProductCreate,
        normalized_name: str,
    ) -> Product:

        db_product = Product(
            product_name=product.product_name,
            normalized_name=normalized_name,
            brand=product.brand,
            category=product.category,
            model_number=product.model_number,
            launch_year=product.launch_year,
            image_url=product.image_url,
        )

        return self.create(
            db=db,
            obj=db_product,
        )

    def update_product(
        self,
        db: Session,
        db_product: Product,
        product: ProductUpdate,
        normalized_name: str,
    ) -> Product:

        db_product.product_name = product.product_name
        db_product.normalized_name = normalized_name
        db_product.brand = product.brand
        db_product.category = product.category
        db_product.model_number = product.model_number
        db_product.launch_year = product.launch_year
        db_product.image_url = product.image_url

        return self.update(
            db=db,
            obj=db_product,
        )

    def get_by_normalized_name(
        self,
        db: Session,
        normalized_name: str,
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(
                Product.normalized_name == normalized_name,
                Product.is_deleted.is_(False),
            )
            .first()
        )

    def get_products(
        self,
        db: Session,
        keyword: str | None = None,
        brand: str | None = None,
        category: ProductCategory | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Product]:

        query = (
            db.query(Product)
            .filter(Product.is_deleted.is_(False))
        )

        if keyword:
            query = query.filter(
                or_(
                    Product.product_name.ilike(f"%{keyword}%"),
                    Product.brand.ilike(f"%{keyword}%"),
                    Product.category.ilike(f"%{keyword}%"),
                )
            )

        if brand:
            query = query.filter(
                Product.brand == brand
            )

        if category:
            query = query.filter(
                Product.category == category
            )

        return (
            query
            .order_by(Product.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def soft_delete(
        self,
        db: Session,
        product: Product,
    ) -> Product:

        product.is_deleted = True
        product.deleted_at = datetime.utcnow()

        return self.update(
            db=db,
            obj=product,
        )

    def restore_product(
        self,
        db: Session,
        product: Product,
    ) -> Product:

        product.is_deleted = False
        product.deleted_at = None

        return self.update(
            db=db,
            obj=product,
        )


product_repository = ProductRepository()