"""SQLAlchemy declarative database models."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Standard SQLAlchemy declarative base class."""


class Course(Base):
    """Represents a golf course/facility."""

    __tablename__ = "course"

    #: Autoincrementing identifier.
    id: Mapped[int] = mapped_column(primary_key=True)

    #: Name of the course.
    name: Mapped[str]

    #: Indicates whether the course is currently open.
    open: Mapped[bool]

    #: Indicates whether the course is public (as opposed to private or
    #: semi-private).
    public: Mapped[bool]

    #: Freeform notes about the course. This is where to enter, for example,
    #: any limitations on the practice areas (e.g. no drivers off the range),
    #: any special instructions for getting to the course, etc.
    notes: Mapped[str | None] = mapped_column(Text)

    #: Indicates whether carts are permitted in the parking lot.
    carts_in_parking_lot: Mapped[bool]

    #: Indicates whether the course has a driving range.
    driving_range: Mapped[bool]

    #: Indicates whether the course has a putting green.
    putting_green: Mapped[bool]

    #: Indicates whether the course has a chipping / pitching / short game
    #: practice area.
    short_game_area: Mapped[bool]

    #: Indicates whether the course has an area for practicing bunker shots.
    bunker_area: Mapped[bool]

    #: Google Maps URL for the course.
    google_maps_link: Mapped[str] = mapped_column(Text)

    #: Drive time as estimated by Google Maps. This is calculated by using
    #: "arrive at" on the next non-holiday Saturday at 10:00am, and taking
    #: the larger of the numbers if it's a range.
    google_maps_drive_time: Mapped[int]

    #: One-to-many :class:`ScorecardNote` relationship.
    scorecard_notes: Mapped[list[ScorecardNote]] = relationship()

    #: One-to-many :class:`Tees` relationship.
    tees: Mapped[list[Tees]] = relationship()


class ScorecardNote(Base):
    """Represents a bullet point (e.g. local rule) on the scorecard."""

    __tablename__ = "scorecard_note"

    #: Autoincrementing identifier.
    id: Mapped[int] = mapped_column(primary_key=True)

    #: Foreign key to :class:`Course`.
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))

    #: Content of the note.
    content: Mapped[str] = mapped_column(Text)

    #: :class:`Course` relationship.
    course: Mapped[Course] = relationship(back_populates="scorecard_notes")


class Tees(Base):
    """Represents a set of tees."""

    __tablename__ = "tees"

    #: Autoincrementing identifier.
    id: Mapped[int] = mapped_column(primary_key=True)

    #: Foreign key to :class:`Course`.
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))

    #: Name of the tees. For example, blue / white / red, or back / middle /
    #: front.
    name: Mapped[str]

    #: Rating for men.
    mens_rating: Mapped[Decimal | None]

    #: Slope for men.
    mens_slope: Mapped[int | None]

    #: Rating for women.
    womens_rating: Mapped[Decimal | None]

    #: Slope for women.
    womens_slope: Mapped[int | None]

    #: :class:`Course` relationship.
    course: Mapped[Course] = relationship(back_populates="tees")

    #: One-to-many :class:`Hole` relationship.
    holes: Mapped[list[Hole]] = relationship()


class Hole(Base):
    """Represents a single hole that is part of a set of tees."""

    __tablename__ = "hole"

    #: Autoincrementing identifier.
    id: Mapped[int] = mapped_column(primary_key=True)

    #: Foreign key to :class:`Tees`.
    tees_id: Mapped[int] = mapped_column(ForeignKey("course.id"))

    #: Length of the hole in yards.
    yardage: Mapped[int]

    #: Par for men.
    mens_par: Mapped[int | None]

    #: Handicap rating for men.
    mens_handicap: Mapped[int | None]

    #: Par for women.
    womens_par: Mapped[int | None]

    #: Handicap rating for women.
    womens_handicap: Mapped[int | None]

    #: :class:`Tees` relationship.
    tees: Mapped[Tees] = relationship(back_populates="holes")
