import re

from bs4 import BeautifulSoup

from app.common.enums import (
    ProductCategory,
    ReviewSource,
)

from app.scraper.amazon.amazon_constants import BASE_URL

from app.scraper.amazon.amazon_utils import (
    build_absolute_url,
    detect_brand,
    detect_category,
    normalize_text,
)

from app.scraper.scraper_dto import (
    ProductDTO,
    ProductDetailDTO,
    ReviewDTO,
)


class AmazonParser:
    """
    Parser responsible for converting Amazon HTML pages
    into DTO objects.
    """

    # ==========================================================
    # Search Page
    # ==========================================================

    @staticmethod
    def parse_products(
        soup: BeautifulSoup,
    ) -> list[ProductDTO]:
        """
        Parse Amazon search results.
        """

        products: list[ProductDTO] = []

        cards = soup.select(
            "div[data-component-type='s-search-result']"
        )

        for card in cards:

            if AmazonParser._is_sponsored(card):
                continue

            title = AmazonParser._extract_title(card)

            url = AmazonParser._extract_product_url(card)

            image = AmazonParser._extract_image(card)

            if not title or not url:
                continue

            products.append(
                ProductDTO(
                    product_name=title,
                    brand=AmazonParser._extract_brand(
                        title
                    ),
                    category=AmazonParser._extract_category(
                        title
                    ),
                    product_url=url,
                    image_url=image,
                )
            )

        return products

    # ==========================================================
    # Product Detail Page
    # ==========================================================

    @staticmethod
    def parse_product_details(
        soup: BeautifulSoup,
        product_url: str,
    ) -> ProductDetailDTO:
        """
        Parse a product detail page.
        """

        product_name = (
            AmazonParser._extract_product_title(
                soup
            )
        )

        brand = (
            AmazonParser._extract_brand(
                product_name
            )
            if product_name
            else None
        )

        category = (
            AmazonParser._extract_category(
                product_name
            )
            if product_name
            else None
        )

        price = AmazonParser._extract_price(
            soup
        )

        mrp = AmazonParser._extract_mrp(
            soup
        )

        discount = (
            AmazonParser._extract_discount(
                soup
            )
        )

        rating = (
            AmazonParser._extract_rating(
                soup
            )
        )

        review_count = (
            AmazonParser._extract_review_count(
                soup
            )
        )

        availability = (
            AmazonParser._extract_availability(
                soup
            )
        )

        description = (
            AmazonParser._extract_description(
                soup
            )
        )

        image = (
            AmazonParser._extract_main_image(
                soup
            )
        )

        return ProductDetailDTO(
            product_name=product_name or "",

            brand=brand,

            category=category,

            price=price,

            mrp=mrp,

            discount_percentage=discount,

            rating=rating,

            review_count=review_count,

            availability=availability,

            description=description,

            image_url=image,

            product_url=product_url,
        )
    
        # ==========================================================
    # Search Page Helper Methods
    # ==========================================================

    @staticmethod
    def _is_sponsored(
        card: BeautifulSoup,
    ) -> bool:
        """
        Check if the search result is sponsored.
        """

        text = card.get_text(
            " ",
            strip=True,
        ).lower()

        return "sponsored" in text

    @staticmethod
    def _extract_title(
        card: BeautifulSoup,
    ) -> str | None:
        """
        Extract product title from search result.
        """

        anchors = card.select("a[href]")

        for anchor in anchors:

            text = normalize_text(
                anchor.get_text(
                    strip=True
                )
            )

            if len(text) > 25:
                return text

        return None

    @staticmethod
    def _extract_product_url(
        card: BeautifulSoup,
    ) -> str | None:
        """
        Extract canonical Amazon product URL.
        """

        anchors = card.select("a[href]")

        for anchor in anchors:

            href = anchor.get("href")

            if not href:
                continue

            if "/dp/" in href:

                return build_absolute_url(
                    href,
                    BASE_URL,
                )

        return None

    @staticmethod
    def _extract_image(
        card: BeautifulSoup,
    ) -> str | None:
        """
        Extract product image from search page.
        """

        image = card.select_one(
            "img.s-image"
        )

        if image:
            return image.get("src")

        return None

    @staticmethod
    def _extract_brand(
        product_name: str,
    ) -> str | None:
        """
        Detect brand from title.
        """

        return detect_brand(
            product_name
        )

    @staticmethod
    def _extract_category(
        product_name: str,
    ) -> ProductCategory | None:
        """
        Detect category from title.
        """

        return detect_category(
            product_name
        )

    # ==========================================================
    # Product Detail Helper Methods
    # ==========================================================

    @staticmethod
    def _extract_product_title(
        soup: BeautifulSoup,
    ) -> str | None:
        """
        Extract product title.
        """

        selectors = [
            "#productTitle",
            "span#productTitle",
            "h1 span",
        ]

        for selector in selectors:

            title = soup.select_one(
                selector
            )

            if title:

                return normalize_text(
                    title.get_text()
                )

        return None

    @staticmethod
    def _extract_main_image(
        soup: BeautifulSoup,
    ) -> str | None:
        """
        Extract main product image.
        """

        image = soup.select_one(
            "#landingImage"
        )

        if image:

            return (
                image.get("data-old-hires")
                or image.get("src")
            )

        return None

    @staticmethod
    def _extract_price(
        soup: BeautifulSoup,
    ) -> float | None:
        """
        Extract selling price.
        """

        selectors = [
            ".apexPriceToPay .a-offscreen",
            ".a-price.aok-align-center .a-offscreen",
            ".a-price .a-offscreen",
        ]

        for selector in selectors:

            element = soup.select_one(
                selector
            )

            if not element:
                continue

            text = (
                element.get_text()
                .replace("₹", "")
                .replace(",", "")
                .strip()
            )

            try:
                return float(text)

            except ValueError:
                continue

        return None

    @staticmethod
    def _extract_mrp(
        soup: BeautifulSoup,
    ) -> float | None:
        """
        Extract MRP.
        """

        selectors = [
            ".a-text-price .a-offscreen",
            "span[data-a-strike='true'] .a-offscreen",
        ]

        for selector in selectors:

            element = soup.select_one(
                selector
            )

            if not element:
                continue

            text = (
                element.get_text()
                .replace("₹", "")
                .replace(",", "")
                .strip()
            )

            try:
                return float(text)

            except ValueError:
                continue

        return None

    @staticmethod
    def _extract_discount(
        soup: BeautifulSoup,
    ) -> float | None:
        """
        Extract discount percentage.
        """

        element = soup.select_one(
            ".savingsPercentage"
        )

        if not element:
            return None

        text = (
            element.get_text()
            .replace("-", "")
            .replace("%", "")
            .strip()
        )

        try:
            return float(text)

        except ValueError:
            return None
        
    @staticmethod
    def _extract_rating(
        soup: BeautifulSoup,
    ) -> float | None:
        """
        Extract overall product rating.
        """

        selectors = [
            "span[data-hook='rating-out-of-text']",
            "#acrPopover span.a-size-base",
            "i.a-icon-star span.a-icon-alt",
        ]

        for selector in selectors:

            element = soup.select_one(selector)

            if not element:
                continue

            text = normalize_text(
                 element.get_text()
            )

            try:
                return float(
                        text.split()[0]
                )

            except (ValueError, IndexError):
                continue

        return None

    @staticmethod
    def _extract_review_count(
        soup: BeautifulSoup,
    ) -> int | None:
        """
        Extract number of ratings/reviews.
        """

        selectors = [
            "#acrCustomerReviewText",
            "span[data-hook='total-review-count']",
        ]

        for selector in selectors:

            element = soup.select_one(selector)

            if not element:
                continue

            text = (
                element.get_text()
                .replace(",", "")
            )

            match = re.search(
                r"\d+",
                text,
            )

            if match:
                return int(match.group())

        return None

    @staticmethod
    def _extract_availability(
        soup: BeautifulSoup,
    ) -> str | None:
        """
        Extract stock availability.
        """

        selectors = [
            "#availability span",
            "#availability",
        ]

        for selector in selectors:

            element = soup.select_one(selector)

            if element:

                text = normalize_text(
                    element.get_text()
                )

                if text:
                    return text

        return None

    @staticmethod
    def _extract_description(
        soup: BeautifulSoup,
    ) -> str | None:
        """
        Extract product description / feature bullets.
        """

        bullets = soup.select(
            "#feature-bullets li span.a-list-item"
        )

        if bullets:

            description = []

            for bullet in bullets:

                text = normalize_text(
                    bullet.get_text()
                )

                if text:
                    description.append(text)

            return "\n".join(description)

        description = soup.select_one(
            "#productDescription"
        )

        if description:

            return normalize_text(
                description.get_text()
            )

        return None
    
    # ==========================================================
    # Review Parser
    # ==========================================================

    @staticmethod
    def parse_reviews(
        soup: BeautifulSoup,
    ) -> list[ReviewDTO]:
        """
        Parse Amazon review cards from both the
        product page preview and review pages.
        """

        reviews: list[ReviewDTO] = []

        review_cards = soup.select(
            "div[data-hook='review']"
        )

        for card in review_cards:

            reviewer = card.select_one(
                ".a-profile-name"
            )

            rating = card.select_one(
                "i[data-hook='review-star-rating'] .a-icon-alt"
            )

            title = (
                card.select_one(
                    "h5[data-hook='reviewTitle']"
                )
                or
                card.select_one(
                    "span[data-hook='review-title']"
                )
            )

            review_text = (
                card.select_one(
                    "div[data-hook='reviewRichContentContainer']"
                )
                or
                card.select_one(
                    "span[data-hook='review-body']"
                )
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

                except Exception:

                    pass

            reviews.append(

                ReviewDTO(

                    source=ReviewSource.AMAZON,

                    reviewer_name=(
                        normalize_text(
                            reviewer.get_text()
                        )
                        if reviewer
                        else None
                    ),

                    rating=rating_value,

                    review_title=(
                        normalize_text(
                            title.get_text()
                        )
                        if title
                        else None
                    ),

                    review_text=normalize_text(
                        review_text.get_text()
                    ),

                    review_date=(
                        normalize_text(
                            review_date.get_text()
                        )
                        if review_date
                        else None
                    ),

                    review_url=None,
                )

            )

        return reviews