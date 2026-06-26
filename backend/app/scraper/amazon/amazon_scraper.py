from urllib.parse import quote_plus

from app.scraper.amazon.amazon_constants import (
    SEARCH_URL,
)

from app.scraper.amazon.amazon_parser import AmazonParser

from app.scraper.base_scraper import BaseScraper

from app.scraper.schemas import (
    ProductDTO,
    ReviewDTO,
)


class AmazonScraper(BaseScraper):
    """
    Amazon scraper implementation.
    """

    def search_product(
        self,
        product_name: str,
    ) -> list[ProductDTO]:
        """
        Search Amazon for a product.
        """

        url = SEARCH_URL.format(
            query=quote_plus(product_name)
        )

        soup = self.fetch_page(url)

        return AmazonParser.parse_products(
            soup=soup,
        )

    def scrape_reviews(
        self,
        product_url: str,
    ) -> list[ReviewDTO]:
        """
        Scrape reviews from an Amazon product page.
        """

        soup = self.fetch_page(
            product_url
        )

        return AmazonParser.parse_reviews(
            soup=soup,
        )