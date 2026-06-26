from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None


class PaginationData(GenericModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: PaginationData[T]