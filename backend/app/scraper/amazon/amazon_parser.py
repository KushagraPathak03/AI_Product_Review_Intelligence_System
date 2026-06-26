from bs4 import BeautifulSoup

from app.scraper.schemas import (
    ProductDTO,
    ReviewDTO,
)

from app.scraper.amazon.amazon_constants import BASE_URL


class AmazonParser:
    """
    Parses Amazon HTML pages into DTO objects.
    """

    @staticmethod
    def parse_products(
        soup: BeautifulSoup,
    ) -> list[ProductDTO]:

        products = []

        product_cards = soup.select(
            "div[data-component-type='s-search-result']"
        )

        for card in product_cards:

            name_element = card.select_one(
                "h2 span"
            )

            link_element = card.select_one(
                "h2 a"
            )

            image_element = card.select_one(
                "img.s-image"
            )

            if not name_element or not link_element:
                continue

            product = ProductDTO(
                product_name=name_element.get_text(strip=True),
                brand=None,
                category=None,
                product_url=BASE_URL + link_element["href"],
                image_url=(
                    image_element["src"]
                    if image_element
                    else None
                ),
            )

            products.append(product)

        return products

    @staticmethod
    def parse_reviews(
        soup: BeautifulSoup,
    ) -> list[ReviewDTO]:

        reviews = []

        review_cards = soup.select(
            "div[data-hook='review']"
        )

        for card in review_cards:

            reviewer = card.select_one(
                "span.a-profile-name"
            )

            rating = card.select_one(
                "i[data-hook='review-star-rating'] span"
            )

            title = card.select_one(
                "a[data-hook='review-title'] span"
            )

            review_text = card.select_one(
                "span[data-hook='review-body']"
            )

            review_date = card.select_one(
                "span[data-hook='review-date']"
            )

            if review_text is None:
                continue

            rating_value = None

            if rating:
                try:
                    rating_value = float(
                        rating.get_text(strip=True).split()[0]
                    )
                except Exception:
                    pass

            review = ReviewDTO(
                source="Amazon",
                reviewer_name=(
                    reviewer.get_text(strip=True)
                    if reviewer
                    else None
                ),
                rating=rating_value,
                review_title=(
                    title.get_text(strip=True)
                    if title
                    else None
                ),
                review_text=review_text.get_text(
                    strip=True
                ),
                review_date=(
                    review_date.get_text(strip=True)
                    if review_date
                    else None
                ),
                review_url=None,
            )

            reviews.append(review)

        return reviews