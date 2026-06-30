import re

from app.common.enums import ProductCategory


KNOWN_BRANDS = {
    "Samsung",
    "Apple",
    "OnePlus",
    "Google",
    "Xiaomi",
    "Redmi",
    "Realme",
    "Oppo",
    "Vivo",
    "Nothing",
    "Motorola",
    "Nokia",
    "Sony",
    "Lenovo",
    "Asus",
    "HP",
    "Dell",
    "Acer",
    "MSI",
    "LG",
    "Boat",
    "JBL",
    "Noise",
    "Fire-Boltt",
    "Honor",
    "Huawei",
}


MODEL_BRAND_MAP = {
    "galaxy": "Samsung",
    "iphone": "Apple",
    "pixel": "Google",
    "oneplus": "OnePlus",
    "redmi": "Xiaomi",
    "xiaomi": "Xiaomi",
    "mi ": "Xiaomi",
    "realme": "Realme",
    "moto": "Motorola",
    "motorola": "Motorola",
    "nothing": "Nothing",
    "boat": "Boat",
    "jbl": "JBL",
    "sony": "Sony",
    "hp": "HP",
    "dell": "Dell",
    "lenovo": "Lenovo",
    "asus": "Asus",
    "acer": "Acer",
}


def normalize_text(
    text: str,
) -> str:
    """
    Remove extra whitespace from text.
    """

    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def detect_brand(
    product_name: str,
) -> str | None:
    """
    Detect product brand from its title.
    """

    title = product_name.lower()

    # Direct brand name detection
    for brand in KNOWN_BRANDS:

        if brand.lower() in title:
            return brand

    # Model family detection
    for keyword, brand in MODEL_BRAND_MAP.items():

        if keyword in title:
            return brand

    return None


def detect_category(
    product_name: str,
) -> ProductCategory | None:
    """
    Detect product category from its title.
    """

    title = product_name.lower()

    if any(
        word in title
        for word in [
            "iphone",
            "galaxy",
            "pixel",
            "smartphone",
            "mobile",
            "phone",
        ]
    ):
        return ProductCategory.SMARTPHONE

    if any(
        word in title
        for word in [
            "laptop",
            "macbook",
            "notebook",
        ]
    ):
        return ProductCategory.LAPTOP

    if any(
        word in title
        for word in [
            "watch",
            "smartwatch",
        ]
    ):
        return ProductCategory.SMARTWATCH

    if any(
        word in title
        for word in [
            "earbuds",
            "buds",
        ]
    ):
        return ProductCategory.EARBUDS

    if any(
        word in title
        for word in [
            "headphones",
            "headset",
        ]
    ):
        return ProductCategory.HEADPHONES

    if any(
        word in title
        for word in [
            "speaker",
            "bluetooth speaker",
        ]
    ):
        return ProductCategory.BLUETOOTH_SPEAKER

    return None


def build_absolute_url(
    url: str,
    base_url: str,
) -> str:
    """
    Convert an Amazon product URL into a clean canonical URL.

    Example:

    https://amazon.in/.../dp/B0DSKNQW8F/ref=...

    becomes

    https://www.amazon.in/dp/B0DSKNQW8F
    """

    if not url:
        return ""

    if not url.startswith("http"):
        url = base_url + url

    match = re.search(
        r"/dp/([A-Z0-9]{10})",
        url,
    )

    if match:

        asin = match.group(1)

        return f"{base_url}/dp/{asin}"

    return url

def extract_asin(
    product_url: str,
) -> str | None:
    """
    Extract Amazon ASIN from a product URL.

    Example:
    https://www.amazon.in/dp/B0FMYC2ZPS

    returns

    B0FMYC2ZPS
    """

    match = re.search(
        r"/dp/([A-Z0-9]{10})",
        product_url,
    )

    if match:
        return match.group(1)

    return None