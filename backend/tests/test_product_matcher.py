from app.scraper.scraper_dto import ProductDTO
from app.scraper.matcher.product_matcher import (
    find_best_product_match,
)

products = [

    ProductDTO(
        product_name="Apple iPhone 17 Pro 512 GB",
        brand="Apple",
        category=None,
        product_url="",
        image_url="",
    ),

    ProductDTO(
        product_name="Apple iPhone 16 Pro 256 GB",
        brand="Apple",
        category=None,
        product_url="",
        image_url="",
    ),

    ProductDTO(
        product_name="Apple iPhone 16 Plus",
        brand="Apple",
        category=None,
        product_url="",
        image_url="",
    ),

]

best = find_best_product_match(
    query="iPhone 16 Pro",
    products=products,
)

print()
print("Best Match")
print(best)