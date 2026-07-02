from rapidfuzz import fuzz

from app.core.logger import get_logger

from app.scraper.matcher.product_parser import (
    ParsedProduct,
    parse_product_name,
)

from app.scraper.scraper_dto import ProductDTO


logger = get_logger(__name__)


MINIMUM_MATCH_SCORE = 65


def _equals(
    left: str | None,
    right: str | None,
) -> bool:
    """
    Compare two strings safely.
    """

    if not left or not right:
        return False

    return (
        left.strip().lower()
        ==
        right.strip().lower()
    )


def calculate_fuzzy_score(
    query: str,
    candidate: str,
) -> float:
    """
    Calculate the best fuzzy similarity.
    """

    return max(
        fuzz.ratio(
            query,
            candidate,
        ),
        fuzz.partial_ratio(
            query,
            candidate,
        ),
        fuzz.token_sort_ratio(
            query,
            candidate,
        ),
        fuzz.token_set_ratio(
            query,
            candidate,
        ),
    )


def calculate_match_score(
    query: ParsedProduct,
    candidate: ParsedProduct,
) -> float:
    """
    Calculate a weighted similarity score.

    Higher score = better match.
    """

    score = 0.0

    # -------------------------------------------------
    # Base Fuzzy Similarity
    # -------------------------------------------------

    fuzzy_score = calculate_fuzzy_score(
        query.normalized_name,
        candidate.normalized_name,
    )

    score += fuzzy_score * 0.40

    # -------------------------------------------------
    # Brand
    # -------------------------------------------------

    if _equals(
        query.brand,
        candidate.brand,
    ):
        score += 15

    # -------------------------------------------------
    # Family
    # -------------------------------------------------

    if _equals(
        query.family,
        candidate.family,
    ):
        score += 20

    # -------------------------------------------------
    # Model
    # -------------------------------------------------

    if (
        query.model
        and candidate.model
    ):

        if _equals(
            query.model,
            candidate.model,
        ):

            score += 35

        else:

            score -= 40

    # -------------------------------------------------
    # Variant
    # -------------------------------------------------

    if (
        query.variant
        and candidate.variant
    ):

        if _equals(
            query.variant,
            candidate.variant,
        ):

            score += 10

        else:

            score -= 5

    # -------------------------------------------------
    # Storage
    # -------------------------------------------------

    if (
        query.storage
        and candidate.storage
    ):

        if _equals(
            query.storage,
            candidate.storage,
        ):

            score += 5

    return round(
        score,
        2,
    )

def find_best_product_match(
    query: str,
    products: list[ProductDTO],
) -> ProductDTO | None:
    """
    Find the best matching product from
    Amazon search results.
    """

    if not products:

        logger.warning(
            "No products available for matching."
        )

        return None

    parsed_query = parse_product_name(
        query
    )

    best_product = None

    best_score = float("-inf")

    best_fuzzy = 0.0

    logger.info(
        "Starting smart product matching."
    )

    logger.debug(
        "Parsed Query: %s",
        parsed_query,
    )

    for product in products:

        parsed_candidate = parse_product_name(
            product.product_name
        )

        fuzzy_score = calculate_fuzzy_score(
            parsed_query.normalized_name,
            parsed_candidate.normalized_name,
        )

        final_score = calculate_match_score(
            parsed_query,
            parsed_candidate,
        )

        logger.debug(
            (
                "Candidate='%s' | "
                "Parsed=%s | "
                "Fuzzy=%.2f | "
                "Score=%.2f"
            ),
            product.product_name,
            parsed_candidate,
            fuzzy_score,
            final_score,
        )

        # -------------------------------------------------
        # Better tie-breaking
        # -------------------------------------------------

        if (
            final_score > best_score
            or (
                final_score == best_score
                and fuzzy_score > best_fuzzy
            )
        ):

            best_score = final_score

            best_fuzzy = fuzzy_score

            best_product = product

    # -------------------------------------------------
    # No Match
    # -------------------------------------------------

    if best_product is None:

        logger.warning(
            "No products available after matching."
        )

        return None

    if best_score < MINIMUM_MATCH_SCORE:

        logger.warning(
            (
                "No suitable product found. "
                "Best Score = %.2f "
                "(Minimum Required = %d)"
            ),
            best_score,
            MINIMUM_MATCH_SCORE,
        )

        return None

    # -------------------------------------------------
    # Selected Product
    # -------------------------------------------------

    logger.info(
        "Selected Product: %s",
        best_product.product_name,
    )

    logger.info(
        (
            "Final Match Score = %.2f | "
            "Fuzzy Score = %.2f"
        ),
        best_score,
        best_fuzzy,
    )

    return best_product