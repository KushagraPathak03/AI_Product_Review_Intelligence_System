from sqlalchemy.orm import Session

from app.product.product_schema import (
    ProductCreate,
    ProductUpdate,
)
from app.product.product_service import (
    ProductService,
)

from app.review.review_schema import (
    ReviewCreate,
)
from app.review.review_service import (
    ReviewService,
)

from app.scraper.amazon.amazon_scraper import (
    AmazonScraper,
)

from app.scraper.matcher.electronic_validator import (
    validate_product_query,
)

from app.scraper.matcher.product_filter import (
    filter_products,
)

from app.scraper.matcher.product_matcher import (
    find_best_product_match,
)

from app.scraper.matcher.strict_matcher import (
    is_strict_match,
)

from app.scraper.matcher.category_detector import (
    detect_category,
)

class ScraperService:
    """
    Coordinates Amazon scraping and database persistence.
    """

    amazon_scraper = AmazonScraper()

    @staticmethod
    def scrape_amazon(
        db: Session,
        product_name: str,
    ):
        """
        Complete Amazon scraping workflow.

        Workflow
        --------
        1. Validate electronic product query.
        2. Search Amazon.
        3. Remove accessories.
        4. Find the best matching product.
        5. Verify the selected product is an exact match.
        6. Scrape product details.
        7. Save or update the product.
        8. Scrape customer reviews.
        9. Save reviews.
        """

        # --------------------------------------------------
        # Validate Product Query
        # --------------------------------------------------

        is_valid, error = validate_product_query(
            product_name
        )

        if not is_valid:

            return {
                "success": False,
                "message": error,
            }

        # --------------------------------------------------
        # Search Amazon
        # --------------------------------------------------

        products = (
            ScraperService.amazon_scraper.search_product(
                product_name
            )
        )

        if not products:

            return {
                "success": False,
                "message": "No products found on Amazon.",
            }

        # --------------------------------------------------
        # Remove Accessories
        # --------------------------------------------------

        products = filter_products(
            products=products,
        )

        if not products:

            return {
                "success": False,
                "message": (
                    "Only accessory listings were found. "
                    "Please search for the electronic product."
                ),
            }

        # --------------------------------------------------
        # Smart Product Matching
        # --------------------------------------------------

        print("\n===== AMAZON SEARCH RESULTS =====")

        for p in products:
            print(p.product_name)

        print("===============================\n")

        product = find_best_product_match(
            query=product_name,
            products=products,
        )

        print("Selected Product:")
        print(product.product_name if product else "None")

        if product is None:

            return {
                "success": False,
                "message": "Requested product was not found on Amazon.",
            }

        # --------------------------------------------------
        # Strict Product Validation
        # --------------------------------------------------

        if not is_strict_match(
            product_name,
            product.product_name,
        ):

            return {
                "success": False,
                "message": (
                    "Requested product was not found on Amazon."
                ),
            }

        # --------------------------------------------------
        # Scrape Product Details
        # --------------------------------------------------

        details = (
            ScraperService.amazon_scraper.scrape_product_details(
                product.product_url
            )
        )

        # --------------------------------------------------
        # Detect Category
        # --------------------------------------------------

        category = (
            details.category
            if details.category
            else detect_category(
                details.product_name
            )
        )

        # --------------------------------------------------
        # Create Product Schema
        # --------------------------------------------------

        product_create = ProductCreate(
            product_name=details.product_name,
            brand=details.brand,
            category=category,
            model_number=None,
            launch_year=None,
            image_url=details.image_url,
            price=details.price,
            mrp=details.mrp,
            discount_percentage=details.discount_percentage,
            rating=details.rating,
            review_count=details.review_count,
            availability=details.availability,
            description=details.description,
            product_url=details.product_url,
        )

        # --------------------------------------------------
        # Save or Update Product
        # --------------------------------------------------

        try:

            db_product = ProductService.create_product(
                db=db,
                product=product_create,
            )

        except Exception:

            existing_products = ProductService.get_products(
                db=db,
                keyword=details.product_name,
                page=1,
                page_size=1,
            )

            if not existing_products:
                raise

            db_product = existing_products[0]

            product_update = ProductUpdate(
                **product_create.model_dump()
            )

            db_product = ProductService.update_product(
                db=db,
                product_id=db_product.id,
                product=product_update,
            )

        # --------------------------------------------------
        # Scrape Reviews
        # --------------------------------------------------

        reviews = (
            ScraperService.amazon_scraper.scrape_reviews(
                details.product_url
            )
        )

        if not reviews:

            return {
                "success": True,
                "message": (
                    "Product found successfully, but no reviews are available."
                ),
                "category": category,
                "product_id": db_product.id,
                "product_name": db_product.product_name,
                "reviews_scraped": 0,
                "reviews_saved": 0,
                "reviews_skipped": 0,
            }

        # --------------------------------------------------
        # Save Reviews
        # --------------------------------------------------

        saved_reviews = 0
        skipped_reviews = 0

        for review in reviews:

            review_create = ReviewCreate(
                product_id=db_product.id,
                source=review.source,
                reviewer_name=review.reviewer_name,
                rating=review.rating,
                review_title=review.review_title,
                review_text=review.review_text,
                review_date=review.review_date,
                review_url=review.review_url,
            )

            try:

                ReviewService.create_review(
                    db=db,
                    review=review_create,
                )

                saved_reviews += 1

            except Exception:

                skipped_reviews += 1

        # --------------------------------------------------
        # Final Response
        # --------------------------------------------------

        return {
            "success": True,
            "message": "Scraping completed successfully.",
            "category": category,
            "product_id": db_product.id,
            "product_name": db_product.product_name,
            "reviews_scraped": len(reviews),
            "reviews_saved": saved_reviews,
            "reviews_skipped": skipped_reviews,
        }


scraper_service = ScraperService()