from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine

# Import models so SQLAlchemy registers them
from app.product.product_model import Product
from app.review.review_model import Review

# Import routers
from app.product.product_routes import (
    router as product_router,
)
from app.review.review_routes import (
    router as review_router,
)
from app.scraper.scraper_routes import (
    router as scraper_router,
)


app = FastAPI(
    title="AI Product Review Intelligence System",
    version="1.0.0",
    description=(
        "AI-powered platform for analyzing electronic product reviews "
        "from Amazon, Flipkart, YouTube, Reddit, and other sources."
    ),
)

# Register API routes
app.include_router(
    product_router,
)

app.include_router(
    review_router,
)

app.include_router(
    scraper_router,
)


@app.get(
    "/",
    tags=["Health"],
)
def home():
    """
    Health check endpoint.
    """

    return {
        "message": "AI Product Review Intelligence API Running",
        "version": "1.0.0",
    }


@app.get(
    "/db-test",
    tags=["Health"],
)
def db_test():
    """
    Test PostgreSQL connection.
    """

    try:

        with engine.connect() as conn:

            version = conn.execute(
                text(
                    "SELECT version();"
                )
            ).scalar()

        return {
            "status": "success",
            "database": "connected",
            "version": version,
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e),
        }