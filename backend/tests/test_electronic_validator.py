from app.scraper.matcher.electronic_validator import (
    validate_product_query,
)

queries = [

    "iPhone 16 Pro",

    "Samsung Galaxy S25 Ultra",

    "MacBook Air M4",

    "Sony WH-1000XM6",

    "Galaxy Watch 8",

    "iPhone Cover",

    "Samsung Charger",

    "Nike Shoes",

]

for query in queries:

    valid, result = validate_product_query(
        query
    )

    print()

    print(query)

    print("Valid :", valid)

    print("Result:", result)