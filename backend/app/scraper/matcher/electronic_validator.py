"""
Basic product query validator.

This validator does NOT check brands or product categories.

Its only responsibility is to reject:
    • Empty queries
    • Very short queries
    • Numeric-only queries
    • Accessories
    • Obvious non-electronic products

Everything else is passed to Amazon search.
"""

import re


INVALID_KEYWORDS = [

    # ----------------------------------
    # Phone / Tablet Accessories
    # ----------------------------------

    "case",
    "cover",
    "back cover",
    "flip cover",
    "bumper",

    "screen protector",
    "screen guard",
    "tempered glass",

    "charger",
    "wireless charger",
    "adapter",

    "cable",
    "usb cable",
    "hdmi cable",
    "type c cable",

    "power bank",

    "holder",
    "mount",
    "tripod",

    "phone stand",
    "tablet stand",
    "laptop stand",

    "skin",

    "keyboard cover",

    "stylus holder",

    "laptop sleeve",

    "watch strap",
    "watch band",

    "ear tips",

    # ----------------------------------
    # Clothing
    # ----------------------------------

    "shoe",
    "shoes",

    "shirt",
    "tshirt",
    "t-shirt",

    "jeans",
    "pant",
    "pants",
    "trouser",

    "wallet",
    "belt",
    "cap",

    # ----------------------------------
    # Furniture
    # ----------------------------------

    "chair",
    "table",
    "desk",
    "bed",
    "sofa",

    # ----------------------------------
    # Kitchen
    # ----------------------------------

    "bottle",
    "cup",
    "mug",

    # ----------------------------------
    # Books
    # ----------------------------------

    "book",

]


def validate_product_query(
    query: str,
) -> tuple[bool, str | None]:
    """
    Validate the user query.

    Returns
    -------
    (True, None)

        Query is allowed.

    (False, error_message)

        Query is invalid.
    """

    # ----------------------------------
    # Empty Query
    # ----------------------------------

    if not query:

        return (
            False,
            "Please enter a product name.",
        )

    query = query.strip().lower()

    if not query:

        return (
            False,
            "Please enter a product name.",
        )

    # ----------------------------------
    # Normalize Spaces
    # ----------------------------------

    query = re.sub(
        r"\s+",
        " ",
        query,
    )

    # ----------------------------------
    # Very Short Query
    # ----------------------------------

    if len(query) < 2:

        return (
            False,
            "Please enter a valid product name.",
        )

    # ----------------------------------
    # Numeric Only
    # ----------------------------------

    if query.isdigit():

        return (
            False,
            "Please enter a valid product name.",
        )

    # ----------------------------------
    # Reject Accessories
    # ----------------------------------

    for keyword in INVALID_KEYWORDS:

        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(
            pattern,
            query,
        ):

            return (
                False,
                "Enter a valid electronic product.",
            )

    # ----------------------------------
    # Allow Everything Else
    #
    # Amazon Search +
    # Smart Matcher +
    # Strict Matcher
    # will determine whether
    # the product exists.
    # ----------------------------------

    return (
        True,
        None,
    )