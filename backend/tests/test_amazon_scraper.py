from app.scraper.amazon.amazon_scraper import AmazonScraper

scraper = AmazonScraper()

products = scraper.search_product(
    "Samsung Galaxy S25 Ultra"
)

print(f"Products Found: {len(products)}")

for product in products[:5]:
    print("-" * 80)
    print(product)