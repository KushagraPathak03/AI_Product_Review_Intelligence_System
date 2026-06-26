import hashlib


def generate_review_hash(
    product_id: int,
    reviewer_name: str | None,
    review_title: str | None,
    review_text: str,
) -> str:
    """
    Generate a deterministic hash for a review.
    """

    data = "|".join(
        [
            str(product_id),
            (reviewer_name or "").strip().lower(),
            (review_title or "").strip().lower(),
            review_text.strip().lower(),
        ]
    )

    return hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()