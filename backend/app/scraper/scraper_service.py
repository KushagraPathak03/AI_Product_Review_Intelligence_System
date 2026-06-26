from sqlalchemy.orm import Session

from app.scraper.amazon.amazon_scraper import AmazonScraper


class ScraperService:
    """
    Coordinates product scraping and review ingestion.
    """

    amazon_scraper = AmazonScraper()

    @staticmethod
    def scrape_amazon(
        db: Session,
        product_name: str,
    ):
        """
        Scrape Amazon product reviews.
        """

        pass