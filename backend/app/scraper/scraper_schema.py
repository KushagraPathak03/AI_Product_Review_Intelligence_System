from pydantic import BaseModel, ConfigDict


class AmazonScrapeRequest(BaseModel):
    """
    Request body for Amazon product scraping.
    """

    product_name: str


class AmazonScrapeResponse(BaseModel):
    """
    Response returned after scraping Amazon reviews.
    """

    product_name: str
    product_created: bool
    reviews_scraped: int
    reviews_saved: int
    duplicates_skipped: int

    model_config = ConfigDict(
        from_attributes=True
    )