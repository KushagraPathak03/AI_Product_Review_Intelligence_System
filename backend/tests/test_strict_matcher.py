from app.scraper.matcher.strict_matcher import (
    is_strict_match,
)


tests = [

    (
        "iPhone 16 Pro",
        "Apple iPhone 16 Pro 256GB",
    ),

    (
        "iPhone 16 Pro",
        "Apple iPhone 17 Pro",
    ),

    (
        "Galaxy S25 Ultra",
        "Samsung Galaxy S25 Ultra 512GB",
    ),

    (
        "Galaxy S25 Ultra",
        "Samsung Galaxy S24 Ultra",
    ),

    (
        "OnePlus 13",
        "OnePlus 13R",
    ),

    (
        "Nothing Phone 3",
        "Nothing Phone 2a",
    ),

]


for query, candidate in tests:

    print()

    print(query)

    print(candidate)

    print(

        is_strict_match(
            query,
            candidate,
        )

    )