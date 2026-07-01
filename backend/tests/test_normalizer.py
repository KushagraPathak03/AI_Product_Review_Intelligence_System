from app.scraper.matcher.normalizer import (
    normalize_product_name,
)


products = [

    "Apple iPhone 17 Pro 512 GB: 6.3″ Display | A19 Pro Chip",

    "Samsung Galaxy S25 Ultra 5G (Titanium Black, 12GB RAM, 256GB Storage)",

    "OnePlus 13 | Smarter with OnePlus AI | 12GB RAM 256GB Storage",

    "REDMI Note 15 5G (Glacier Blue, 8GB RAM, 128GB Storage)",

]

for p in products:

    print()

    print("Original : ", p)

    print(
        "Normalized:",
        normalize_product_name(
            p
        )
    )