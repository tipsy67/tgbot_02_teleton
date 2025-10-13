"""delete uniq api_id

Revision ID: 283ce232a2bc
Revises: 89a7722c9d98
Create Date: 2025-10-10 23:53:12.443777

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "283ce232a2bc"
down_revision: Union[str, Sequence[str], None] = "89a7722c9d98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("sessions", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.drop_constraint(op.f("uq_sessions_api_id"), "sessions", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        op.f("uq_sessions_api_id"),
        "sessions",
        ["api_id"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column("sessions", "created_at")
