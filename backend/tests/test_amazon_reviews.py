from app.scraper.amazon.amazon_scraper import (
    AmazonScraper,
)


def main():

    scraper = AmazonScraper()

    products = scraper.search_product(
        "Samsung Galaxy S25 Ultra"
    )

    if not products:
        print("No products found.")
        return

    reviews = scraper.scrape_reviews(
        products[0].product_url
    )

    print(
        f"Reviews Found: {len(reviews)}"
    )

    for review in reviews[:5]:

        print("-" * 80)

        print(review)


if __name__ == "__main__":
    main()