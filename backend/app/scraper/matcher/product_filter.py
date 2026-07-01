"""
Generic product filter.

Removes accessory listings from Amazon search results.

This filter does NOT determine product categories.
Its only responsibility is to remove accessories
and keep potential electronic products.

The product matcher is responsible for selecting
the correct product.
"""

from app.scraper.scraper_dto import ProductDTO


ACCESSORY_KEYWORDS = [

    # Phone accessories
    "cover",
    "case",
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

    # More specific stand keywords
    "phone stand",
    "tablet stand",
    "laptop stand",

    "skin",

    # Laptop accessories
    "laptop sleeve",
    "sleeve",

    # Watch accessories
    "watch strap",
    "watch band",
    "strap",
    "band",

    # Earbud accessories
    "ear tips",

]


def filter_products(
    products: list[ProductDTO],
) -> list[ProductDTO]:
    """
    Remove obvious accessories from
    Amazon search results.
    """

    filtered_products = []

    for product in products:

        name = product.product_name.lower().strip()

        is_accessory = False

        for keyword in ACCESSORY_KEYWORDS:

            if keyword in name:

                is_accessory = True
                break

        if is_accessory:
            continue

        filtered_products.append(product)

    return filtered_products