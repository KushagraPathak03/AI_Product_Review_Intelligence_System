"""
Constants used by the Amazon scraper.
"""

BASE_URL = "https://www.amazon.in"

# ---------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------

SEARCH_URL = (
    BASE_URL + "/s?k={query}"
)

# ---------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------

REVIEW_URL = (
    BASE_URL + "/product-reviews/{asin}"
)

# ---------------------------------------------------------------------
# HTTP Headers
# ---------------------------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    ),
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}