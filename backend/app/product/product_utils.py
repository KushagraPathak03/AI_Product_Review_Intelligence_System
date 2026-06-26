def normalize_product_name(product_name: str) -> str:
    """
    Normalize a product name for duplicate detection and searching.
    """

    return " ".join(
        product_name.lower().strip().split()
    )