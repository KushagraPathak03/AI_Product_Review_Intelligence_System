from typing import Generic, Type, TypeVar

from sqlalchemy.orm import Session

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository containing common database operations.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_by_id(
        self,
        db: Session,
        obj_id: int,
        include_deleted: bool = False,
    ) -> ModelType | None:

        query = (
            db.query(self.model)
            .filter(self.model.id == obj_id)
        )

        # Automatically ignore soft-deleted records
        if (
            hasattr(self.model, "is_deleted")
            and not include_deleted
        ):
            query = query.filter(
                self.model.is_deleted.is_(False)
            )

        return query.first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[ModelType]:

        query = db.query(self.model)

        if (
            hasattr(self.model, "is_deleted")
            and not include_deleted
        ):
            query = query.filter(
                self.model.is_deleted.is_(False)
            )

        return (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:

        db.commit()
        db.refresh(obj)
        return obj

    def delete(
        self,
        db: Session,
        obj: ModelType,
    ) -> None:

        db.delete(obj)
        db.commit()

    def exists(
        self,
        db: Session,
        **filters,
    ) -> bool:

        query = db.query(self.model).filter_by(
            **filters
        )

        if hasattr(self.model, "is_deleted"):
            query = query.filter(
                self.model.is_deleted.is_(False)
            )

        return query.first() is not None