from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.scraper.scraper_service import scraper_service


router = APIRouter(
    prefix="/scraper",
    tags=["Scraper"],
)


class AmazonScrapeRequest(BaseModel):
    product_name: str


@router.post(
    "/amazon/search",
)
def scrape_amazon(
    request: AmazonScrapeRequest,
    db: Session = Depends(get_db),
):
    """
    Search Amazon, save the product and
    reviews into the database.
    """

    return scraper_service.scrape_amazon(
        db=db,
        product_name=request.product_name,
    )