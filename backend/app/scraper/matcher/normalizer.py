"""
Normalize product names before matching.

This module removes marketing noise while preserving
important product identifiers such as model numbers,
variants, storage sizes, and product families.
"""

import re


# ---------------------------------------------------------
# Marketing phrases that add little value for matching.
# ---------------------------------------------------------

REMOVE_PHRASES = [

    "official",

    "latest model",
    "latest edition",
    "new launch",
    "new arrival",

    "best seller",

    "with charger",
    "without charger",

    "dual sim",
    "single sim",

    "factory unlocked",
    "unlocked",

    "amazon choice",

]


def normalize_product_name(
    product_name: str,
) -> str:
    """
    Normalize a product title.

    Example
    -------

    Apple iPhone 16 Pro (256 GB) :
    5G Smartphone | A18 Pro Chip

    becomes

    apple iphone 16 pro 256gb 5g smartphone a18 pro chip
    """

    if not product_name:

        return ""

    text = product_name.lower()

    # -----------------------------------------------------
    # Replace separators with spaces
    # -----------------------------------------------------

    separators = [

        "|",
        "/",
        "\\",
        ",",
        ";",
        ":",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",

    ]

    for separator in separators:

        text = text.replace(
            separator,
            " ",
        )

    # -----------------------------------------------------
    # Remove marketing phrases
    # -----------------------------------------------------

    for phrase in REMOVE_PHRASES:

        text = text.replace(
            phrase,
            " ",
        )

    # -----------------------------------------------------
    # Normalize storage
    #
    # 512 GB -> 512gb
    # 1 TB   -> 1tb
    # -----------------------------------------------------

    text = re.sub(
        r"(\d+)\s*gb",
        r"\1gb",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"(\d+)\s*tb",
        r"\1tb",
        text,
        flags=re.IGNORECASE,
    )

    # -----------------------------------------------------
    # Preserve hyphens inside model numbers
    #
    # WH-1000XM6
    # WF-1000XM5
    # PD-3225U
    # -----------------------------------------------------

    text = re.sub(
        r"[^\w\s\-]",
        " ",
        text,
    )

    # -----------------------------------------------------
    # Remove duplicate spaces
    # -----------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()