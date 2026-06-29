from app.scraper.amazon.amazon_scraper import AmazonScraper


def main():

    scraper = AmazonScraper()

    products = scraper.search_product(
        "Samsung Galaxy S25 Ultra"
    )

    if not products:
        print("No products found.")
        return

    product = scraper.scrape_product_details(
        products[0].product_url
    )

    print(product)


if __name__ == "__main__":
    main()