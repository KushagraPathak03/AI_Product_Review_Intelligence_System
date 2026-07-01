import re
from dataclasses import dataclass

from app.scraper.matcher.normalizer import (
    normalize_product_name,
)


@dataclass
class ParsedProduct:
    """
    Structured representation of a product.
    """

    brand: str | None = None
    family: str | None = None
    model: str | None = None
    variant: str | None = None
    storage: str | None = None
    color: str | None = None
    normalized_name: str = ""


# ----------------------------------------------------
# Generic product families
# ----------------------------------------------------

FAMILIES = {

    "iphone",
    "galaxy",
    "pixel",

    "macbook",
    "ipad",

    "watch",
    "airpods",
    "buds",
    "earbuds",
    "headphones",

    "laptop",
    "notebook",
    "tablet",

    "monitor",
    "camera",

    "playstation",
    "xbox",
    "switch",
    "console",

    "tv",

}


# ----------------------------------------------------
# Words ignored while detecting brands
# ----------------------------------------------------

IGNORED_WORDS = {

    "new",
    "latest",
    "official",
    "edition",
    "series",

    "wireless",
    "bluetooth",

    "smart",

    "with",
    "and",
    "for",
    "the",

    "true",
    "truly",

    "noise",
    "cancelling",

    "premium",
    "original",

    "fast",

    "gb",
    "tb",

}


# ----------------------------------------------------
# Common variants
# ----------------------------------------------------

VARIANTS = [

    "ultra",

    "pro max",

    "pro",

    "plus",

    "fe",

    "ce",

    "lite",

    "mini",

    "air",

    "flip",

    "fold",

]


STORAGE_PATTERN = re.compile(
    r"(\d+)\s?(gb|tb)",
    re.IGNORECASE,
)


MODEL_PATTERN = re.compile(
    r"\b([a-z]{0,5}\d+[a-z0-9\-]*)\b",
    re.IGNORECASE,
)


def parse_product_name(
    product_name: str,
) -> ParsedProduct:
    """
    Parse a product title into structured
    information.

    Works for ANY electronic brand.
    """

    normalized = normalize_product_name(
        product_name
    )

    parsed = ParsedProduct(
        normalized_name=normalized,
    )

    words = normalized.split()

    # ------------------------------------------------
    # Product Family
    # ------------------------------------------------

    for word in words:

        if word in FAMILIES:

            parsed.family = word.title()
            break

    # ------------------------------------------------
    # Brand
    #
    # Brand = first meaningful word before
    # the detected family.
    # ------------------------------------------------

    if parsed.family:

        family_index = words.index(
            parsed.family.lower()
        )

        if family_index > 0:

            candidate = words[
                family_index - 1
            ]

            if (
                candidate not in IGNORED_WORDS
                and not candidate.isdigit()
            ):

                parsed.brand = candidate.title()

    else:

        for word in words:

            if (

                word not in IGNORED_WORDS

                and word not in FAMILIES

                and not word.isdigit()

                and len(word) > 1

            ):

                parsed.brand = word.title()
                break

    # ------------------------------------------------
    # Storage
    # ------------------------------------------------

    storage = STORAGE_PATTERN.search(
        normalized
    )

    if storage:

        parsed.storage = (
            storage.group(1)
            + storage.group(2).upper()
        )

    # ------------------------------------------------
    # Variant
    # ------------------------------------------------

    for variant in sorted(
        VARIANTS,
        key=len,
        reverse=True,
    ):

        if variant in normalized:

            parsed.variant = (
                variant.title()
            )

            break

    # ------------------------------------------------
    # Model Number
    # ------------------------------------------------

    model = MODEL_PATTERN.search(
        normalized
    )

    if model:

        parsed.model = (
            model.group(1)
            .upper()
        )

    return parsed