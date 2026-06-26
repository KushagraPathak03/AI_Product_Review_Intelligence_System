"""
Constants used by the Amazon scraper.
"""

BASE_URL = "https://www.amazon.in"

SEARCH_URL = (
    BASE_URL + "/s?k={query}"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}