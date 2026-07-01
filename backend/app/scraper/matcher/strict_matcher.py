"""
Strict product validation.

The smart matcher finds the closest Amazon product.
This module verifies that the selected product
actually represents the product requested by the user.

The matcher is intentionally strict about product
identity (family, model, variant), while ignoring
marketing words, colours, storage size, etc.

This implementation is brand-independent and works
with any electronic brand.
"""

import re

from rapidfuzz import fuzz

from app.scraper.matcher.product_parser import (
    parse_product_name,
)


# Words that should not influence matching.
IGNORED_WORDS = {
    "new",
    "latest",
    "wireless",
    "bluetooth",
    "smart",
    "official",
    "edition",
    "series",
    "premium",
    "original",
    "fast",
    "with",
    "and",
    "for",
    "the",
    "tws",
    "true",
    "truly",
    "anc",
    "enc",
    "noise",
    "cancelling",
    "color",
    "colour",
}


MINIMUM_SIMILARITY = 80


def _normalize(
    text: str | None,
) -> str:
    """
    Normalize text before comparison.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9 ]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def _is_equal(
    left: str | None,
    right: str | None,
) -> bool:
    """
    Case-insensitive comparison.
    """

    return (
        _normalize(left)
        == _normalize(right)
    )


def is_strict_match(
    query: str,
    candidate: str,
) -> bool:
    """
    Validate whether the selected Amazon
    product is actually the requested product.
    """

    query_product = parse_product_name(
        query
    )

    candidate_product = parse_product_name(
        candidate
    )

    # --------------------------------------------------
    # Brand
    #
    # Compare only when BOTH brands are available.
    # --------------------------------------------------

    if (
        query_product.brand
        and candidate_product.brand
        and not _is_equal(
            query_product.brand,
            candidate_product.brand,
        )
    ):
        return False

    # --------------------------------------------------
    # Family
    # --------------------------------------------------

    if (
        query_product.family
        and candidate_product.family
        and not _is_equal(
            query_product.family,
            candidate_product.family,
        )
    ):
        return False

    # --------------------------------------------------
    # Model
    #
    # Wrong model means wrong product.
    # --------------------------------------------------

    if (
        query_product.model
        and candidate_product.model
        and not _is_equal(
            query_product.model,
            candidate_product.model,
        )
    ):
        return False

    # --------------------------------------------------
    # Variant
    #
    # Ignore marketing words.
    # --------------------------------------------------

    query_variant = _normalize(
        query_product.variant
    )

    candidate_variant = _normalize(
        candidate_product.variant
    )

    if (
        query_variant
        and candidate_variant
        and query_variant not in IGNORED_WORDS
        and candidate_variant not in IGNORED_WORDS
        and query_variant != candidate_variant
    ):
        return False

    # --------------------------------------------------
    # Final similarity check
    #
    # Prevents accepting unrelated products even if
    # parsing is incomplete.
    # --------------------------------------------------

    similarity = fuzz.token_set_ratio(
        query_product.normalized_name,
        candidate_product.normalized_name,
    )

    if similarity < MINIMUM_SIMILARITY:

        return False

    return True