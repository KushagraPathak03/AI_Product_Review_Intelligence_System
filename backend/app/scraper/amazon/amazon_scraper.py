from urllib.parse import quote_plus

from app.scraper.amazon.amazon_constants import (
    SEARCH_URL,
)

from app.scraper.amazon.amazon_parser import (
    AmazonParser,
)

from app.scraper.base_scraper import (
    BaseScraper,
)

from app.scraper.scraper_dto import (
    ProductDTO,
    ProductDetailDTO,
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
        Search Amazon for products.
        """

        url = SEARCH_URL.format(
            query=quote_plus(product_name)
        )

        soup = self.fetch_page(
            url
        )

        return AmazonParser.parse_products(
            soup
        )

    def scrape_product_details(
        self,
        product_url: str,
    ) -> ProductDetailDTO:
        """
        Scrape detailed product information.
        """

        soup = self.fetch_page(
            product_url
        )

        return AmazonParser.parse_product_details(
            soup=soup,
            product_url=product_url,
        )

    def scrape_reviews(
        self,
        product_url: str,
    ) -> list[ReviewDTO]:
        """
        Scrape reviews from a product page.
        """

        soup = self.fetch_page(
            product_url
        )

        return AmazonParser.parse_reviews(
            soup
        )