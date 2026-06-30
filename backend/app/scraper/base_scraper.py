from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

from app.scraper.scraper_dto import (
    ProductDTO,
    ReviewDTO,
)


class BaseScraper(ABC):
    """
    Base class for all website scrapers.

    Uses Playwright to fetch fully rendered HTML
    and converts it into BeautifulSoup.
    """

    HEADLESS = True

    TIMEOUT = 30000

    WAIT_UNTIL = "domcontentloaded"

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )

    def get_page_html(
        self,
        url: str,
    ) -> str:
        """
        Open a webpage using Playwright and
        return its rendered HTML.
        """

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=self.HEADLESS,
            )

            context = browser.new_context(
                user_agent=self.USER_AGENT,
                viewport={
                    "width": 1920,
                    "height": 1080,
                },
            )

            page = context.new_page()

            try:

                page.goto(
                    url,
                    wait_until=self.WAIT_UNTIL,
                    timeout=self.TIMEOUT,
                )

                page.wait_for_timeout(
                    3000
                )

                html = page.content()

            except PlaywrightTimeoutError:

                html = page.content()

            finally:

                browser.close()

        return html

    def fetch_page(
        self,
        url: str,
    ) -> BeautifulSoup:
        """
        Download a webpage and return BeautifulSoup.
        """

        html = self.get_page_html(
            url
        )

        return BeautifulSoup(
            html,
            "html.parser",
        )

    def fetch_reviews_page(
        self,
        product_url: str,
    ) -> BeautifulSoup:
        """
        Open the product page and click the
        'See all reviews' link using Playwright.
        """

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=self.HEADLESS,
            )

            context = browser.new_context(
                user_agent=self.USER_AGENT,
                viewport={
                    "width": 1920,
                    "height": 1080,
                },
            )

            page = context.new_page()

            try:

                page.goto(
                    product_url,
                    wait_until=self.WAIT_UNTIL,
                    timeout=self.TIMEOUT,
                )

                page.wait_for_timeout(
                    3000
                )

                selectors = [
                    "#acrCustomerReviewLink",
                    "a[data-hook='see-all-reviews-link-foot']",
                    "a[href*='product-reviews']",
                ]

                clicked = False

                for selector in selectors:

                    try:

                        locator = page.locator(selector)

                        if locator.count() > 0:

                            locator.first.click()

                            clicked = True

                            break

                    except Exception:

                        continue

                if clicked:

                    page.wait_for_timeout(
                        5000
                    )

                html = page.content()

            except PlaywrightTimeoutError:

                html = page.content()

            finally:

                browser.close()

        return BeautifulSoup(
            html,
            "html.parser",
        )

    @abstractmethod
    def search_product(
        self,
        product_name: str,
    ) -> list[ProductDTO]:
        pass

    @abstractmethod
    def scrape_reviews(
        self,
        product_url: str,
    ) -> list[ReviewDTO]:
        pass