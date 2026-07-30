"""create_initial_tables"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7061ef8dc7e2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Creates the initial tables for FastTrack."""
    op.create_table(
        "packages",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("recipient_name", sa.String(255), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("access_cost", sa.Float(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "vehicles",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("plate", sa.String(20), nullable=False),
        sa.Column("max_weight", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plate"),
    )

    op.create_table(
        "hubs",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column(
            "is_central", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "hub_packages",
        sa.Column("hub_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("package_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["hub_id"], ["hubs.id"]),
        sa.ForeignKeyConstraint(["package_id"], ["packages.id"]),
        sa.PrimaryKeyConstraint("hub_id", "package_id"),
    )


def downgrade() -> None:
    """Drops all tables created in upgrade()."""
    op.drop_table("hub_packages")
    op.drop_table("hubs")
    op.drop_table("vehicles")
    op.drop_table("packages")
