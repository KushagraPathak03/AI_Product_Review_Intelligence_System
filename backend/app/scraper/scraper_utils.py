from rapidfuzz import fuzz

from app.scraper.scraper_dto import ProductDTO


MINIMUM_MATCH_SCORE = 80


def find_best_product_match(
    query: str,
    products: list[ProductDTO],
) -> ProductDTO | None:
    """
    Find the best matching product for the user's query.

    Combines multiple RapidFuzz scoring algorithms
    for improved matching accuracy.
    """

    if not products:
        return None

    query = query.lower().strip()

    best_product = None
    best_score = 0

    print("\nMatching Products")
    print("-" * 100)

    for product in products:

        product_name = product.product_name.lower().strip()

        score = max(
            fuzz.ratio(query, product_name),
            fuzz.partial_ratio(query, product_name),
            fuzz.token_sort_ratio(query, product_name),
            fuzz.token_set_ratio(query, product_name),
        )

        print(
            f"{score:6.2f}%  ->  {product.product_name}"
        )

        if score > best_score:
            best_score = score
            best_product = product

    print("-" * 100)

    if best_score < MINIMUM_MATCH_SCORE:

        print(
            f"No suitable product found "
            f"(Best Score: {best_score:.2f}%)"
        )

        return None

    print(
        f"Selected ({best_score:.2f}%): "
        f"{best_product.product_name}"
    )

    print("-" * 100)

    return best_product