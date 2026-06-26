from bs4 import BeautifulSoup

from app.common.enums import ReviewSource

from app.scraper.amazon.amazon_constants import BASE_URL
from app.scraper.scraper_dto import (
    ProductDTO,
    ReviewDTO,
)


class AmazonParser:
    """
    Parses Amazon HTML pages into ProductDTO and ReviewDTO objects.
    """

    @staticmethod
    def parse_products(
        soup: BeautifulSoup,
    ) -> list[ProductDTO]:
        """
        Parse Amazon search results into ProductDTO objects.
        """

        products: list[ProductDTO] = []

        product_cards = soup.select(
            "div[data-component-type='s-search-result']"
        )

        for card in product_cards:

            # Skip sponsored products
            sponsored = card.select_one(
                "span.s-sponsored-label-text"
            )

            if sponsored:
                continue

            image_element = card.select_one(
                "img.s-image"
            )

            title_anchor = None

            #
            # Amazon changes its HTML frequently.
            # Try multiple selectors in order.
            #
            selectors = [
                "a.a-link-normal.s-line-clamp-2",
                "a.a-link-normal.s-no-outline",
                "div[data-cy='title-recipe'] a",
                "h2 + a",
            ]

            for selector in selectors:
                title_anchor = card.select_one(
                    selector
                )

                if (
                    title_anchor
                    and title_anchor.get_text(strip=True)
                ):
                    break

            #
            # Fallback
            #
            if title_anchor is None:

                for anchor in card.select("a[href]"):

                    text = anchor.get_text(
                        strip=True
                    )

                    if len(text) > 20:
                        title_anchor = anchor
                        break

            if title_anchor is None:
                continue

            product_name = title_anchor.get_text(
                strip=True
            )

            product_url = title_anchor.get(
                "href"
            )

            if not product_url:
                continue

            if not product_url.startswith(
                "http"
            ):
                product_url = (
                    BASE_URL + product_url
                )

            product = ProductDTO(
                product_name=product_name,
                brand=None,
                category=None,
                product_url=product_url,
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
        """
        Parse an Amazon review page into ReviewDTO objects.
        """

        reviews: list[ReviewDTO] = []

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
                        rating.get_text(
                            strip=True
                        ).split()[0]
                    )
                except ValueError:
                    rating_value = None

            review = ReviewDTO(
                source=ReviewSource.AMAZON,
                reviewer_name=(
                    reviewer.get_text(
                        strip=True
                    )
                    if reviewer
                    else None
                ),
                rating=rating_value,
                review_title=(
                    title.get_text(
                        strip=True
                    )
                    if title
                    else None
                ),
                review_text=review_text.get_text(
                    strip=True
                ),
                review_date=(
                    review_date.get_text(
                        strip=True
                    )
                    if review_date
                    else None
                ),
                review_url=None,
            )

            reviews.append(review)

        return reviews