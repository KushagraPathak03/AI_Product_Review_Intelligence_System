from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from app.scraper.schemas import (
    ProductDTO,
    ReviewDTO,
)


class BaseScraper(ABC):
    """
    Base class for all website scrapers.
    """

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )

    def __init__(self):
        self.headers = {
            "User-Agent": self.USER_AGENT,
        }

    def fetch_page(
        self,
        url: str,
    ) -> BeautifulSoup:
        """
        Download a webpage and return a BeautifulSoup object.
        """

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return BeautifulSoup(
            response.text,
            "html.parser",
        )

    @abstractmethod
    def search_product(
        self,
        product_name: str,
    ) -> list[ProductDTO]:
        """
        Search for products and return matching products.
        """
        pass

    @abstractmethod
    def scrape_reviews(
        self,
        product_url: str,
    ) -> list[ReviewDTO]:
        """
        Scrape reviews from a product page.
        """
        pass