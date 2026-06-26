"""Add review hash

Revision ID: f46d7050d99b
Revises: a05a16d5f7e9
Create Date: 2026-06-26 14:52:46.906711
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f46d7050d99b"
down_revision: Union[str, Sequence[str], None] = "a05a16d5f7e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Step 1: Add the column as nullable
    op.add_column(
        "reviews",
        sa.Column(
            "review_hash",
            sa.String(length=64),
            nullable=True,
        ),
    )

    # Step 2: Populate existing rows
    op.execute(
        """
        UPDATE reviews
        SET review_hash = md5(id::text || review_text)
        """
    )

    # Step 3: Make the column NOT NULL
    op.alter_column(
        "reviews",
        "review_hash",
        nullable=False,
    )

    # Step 4: Create unique index
    op.create_index(
        "ix_reviews_review_hash",
        "reviews",
        ["review_hash"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_reviews_review_hash",
        table_name="reviews",
    )

    op.drop_column(
        "reviews",
        "review_hash",
    )