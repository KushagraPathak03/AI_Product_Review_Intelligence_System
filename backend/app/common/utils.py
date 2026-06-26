import re
import unicodedata


def normalize_product_name(name: str) -> str:
    """
    Normalize product names for searching and duplicate detection.

    Example:
    Samsung Galaxy S25 Ultra
        ↓
    samsung galaxy s25 ultra
    """

    # Remove unicode accents
    name = unicodedata.normalize("NFKD", name)

    # lowercase
    name = name.lower()

    # remove leading/trailing spaces
    name = name.strip()

    # collapse multiple spaces
    name = re.sub(r"\s+", " ", name)

    return name