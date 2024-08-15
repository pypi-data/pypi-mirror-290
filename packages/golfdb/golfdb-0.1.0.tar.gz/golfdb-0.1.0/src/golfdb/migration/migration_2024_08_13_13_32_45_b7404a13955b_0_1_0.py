"""Initial migration."""

from __future__ import annotations

import typing

import alembic
import sqlalchemy as sa

revision: str = "b7404a13955b"
down_revision: str | None = None
branch_labels: str | typing.Sequence[str] | None = None
depends_on: str | typing.Sequence[str] | None = None


def upgrade() -> None:
    """Perform operations for the upgrade."""
    alembic.op.create_table(
        "course",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("open", sa.Boolean(), nullable=False),
        sa.Column("public", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("carts_in_parking_lot", sa.Boolean(), nullable=False),
        sa.Column("driving_range", sa.Boolean(), nullable=False),
        sa.Column("putting_green", sa.Boolean(), nullable=False),
        sa.Column("short_game_area", sa.Boolean(), nullable=False),
        sa.Column("bunker_area", sa.Boolean(), nullable=False),
        sa.Column("google_maps_link", sa.Text(), nullable=False),
        sa.Column("google_maps_drive_time", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    alembic.op.create_table(
        "scorecard_note",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["course.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    alembic.op.create_table(
        "tees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("mens_rating", sa.Numeric(), nullable=True),
        sa.Column("mens_slope", sa.Integer(), nullable=True),
        sa.Column("womens_rating", sa.Numeric(), nullable=True),
        sa.Column("womens_slope", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["course_id"], ["course.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    alembic.op.create_table(
        "hole",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tees_id", sa.Integer(), nullable=False),
        sa.Column("yardage", sa.Integer(), nullable=False),
        sa.Column("mens_par", sa.Integer(), nullable=True),
        sa.Column("mens_handicap", sa.Integer(), nullable=True),
        sa.Column("womens_par", sa.Integer(), nullable=True),
        sa.Column("womens_handicap", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["tees_id"], ["course.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Perform operations for the downgrade."""
    alembic.op.drop_table("hole")
    alembic.op.drop_table("tees")
    alembic.op.drop_table("scorecard_note")
    alembic.op.drop_table("course")
