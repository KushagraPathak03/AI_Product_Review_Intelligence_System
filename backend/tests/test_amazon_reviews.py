scraper = AmazonScraper()

products = scraper.search_product(
    "Samsung Galaxy S25 Ultra"
)

reviews = scraper.scrape_reviews(
    products[0].product_url
)

print(reviews[:5])