from app.scraper.matcher.product_parser import (
    parse_product_name,
)


products = [

    "Apple iPhone 17 Pro 512 GB",

    "Apple iPhone 16 Pro 256 GB",

    "Samsung Galaxy S25 Ultra 256 GB",

    "Samsung Galaxy S24 FE",

    "OnePlus 13 256 GB",

    "Nothing Phone 3",

    "Nothing Phone 3a Pro",

    "Redmi Note 15 Pro 512 GB",

]

for product in products:

    parsed = parse_product_name(
        product
    )

    print()

    print("=" * 60)

    print(product)

    print(parsed)