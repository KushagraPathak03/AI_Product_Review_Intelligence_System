from urllib.parse import quote_plus

from app.scraper.amazon.amazon_constants import SEARCH_URL
from app.scraper.base_scraper import BaseScraper


class TestScraper(BaseScraper):

    def search_product(self, product_name):
        pass

    def scrape_reviews(self, product_url):
        pass


def main():

    scraper = TestScraper()

    url = SEARCH_URL.format(
        query=quote_plus("Samsung Galaxy S25 Ultra")
    )

    soup = scraper.fetch_page(url)

    print(
        soup.title.get_text(strip=True)
    )

    print(
        len(
            soup.select(
                "div[data-component-type='s-search-result']"
            )
        )
    )


if __name__ == "__main__":
    main()