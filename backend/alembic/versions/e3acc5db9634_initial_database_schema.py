"""Initial database schema

Revision ID: e3acc5db9634
Revises:
Create Date: 2026-06-25 19:58:19.901522
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3acc5db9634"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # -------------------------
    # Products Table
    # -------------------------
    op.create_table(
        "products",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "product_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "normalized_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "brand",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "model_number",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "launch_year",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "image_url",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_products_brand"),
        "products",
        ["brand"],
        unique=False,
    )

    op.create_index(
        op.f("ix_products_category"),
        "products",
        ["category"],
        unique=False,
    )

    op.create_index(
        op.f("ix_products_id"),
        "products",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_products_normalized_name"),
        "products",
        ["normalized_name"],
        unique=True,
    )

    # -------------------------
    # Reviews Table
    # -------------------------
    op.create_table(
        "reviews",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "source",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "reviewer_name",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "rating",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "review_title",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "review_text",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "sentiment",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "review_date",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "review_url",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_reviews_id"),
        "reviews",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_reviews_product_id"),
        "reviews",
        ["product_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_reviews_source"),
        "reviews",
        ["source"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_reviews_source"),
        table_name="reviews",
    )

    op.drop_index(
        op.f("ix_reviews_product_id"),
        table_name="reviews",
    )

    op.drop_index(
        op.f("ix_reviews_id"),
        table_name="reviews",
    )

    op.drop_table("reviews")

    op.drop_index(
        op.f("ix_products_normalized_name"),
        table_name="products",
    )

    op.drop_index(
        op.f("ix_products_id"),
        table_name="products",
    )

    op.drop_index(
        op.f("ix_products_category"),
        table_name="products",
    )

    op.drop_index(
        op.f("ix_products_brand"),
        table_name="products",
    )

    op.drop_table("products")