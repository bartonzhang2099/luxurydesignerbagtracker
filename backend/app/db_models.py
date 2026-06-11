"""
Phase 5.5: SQLAlchemy ORM models.

Concepts: ORM mapping (Python classes <-> SQL tables), columns and types,
primary/foreign keys, one-to-many relationships.

These mirror `app.models.Bag` / `PricePoint`, but as database tables:
- `bags` (one row per bag listing)
- `price_points` (many rows per bag - its price history), each with a
  `bag_id` foreign key back to `bags.id`.
"""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from app.db import Base
from app.models import BagCondition


class BagORM(Base):
    """The `bags` table."""

    __tablename__ = "bags"

    id = Column(String, primary_key=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    color = Column(String, nullable=False)
    condition = Column(SAEnum(BagCondition), nullable=False)
    source = Column(String, nullable=False)

    # TODO: define a one-to-many relationship to `PricePointORM`.
    #
    # Hints:
    # - `relationship("PricePointORM", back_populates="bag", ...)`
    # - Pass `order_by="PricePointORM.timestamp"` so `.price_history` comes
    #   back oldest -> newest, matching `Bag.price_history`.
    # - Pass `cascade="all, delete-orphan"` so deleting a `BagORM` also
    #   deletes its price points.
    price_history = None  # replace with `relationship(...)`


class PricePointORM(Base):
    """The `price_points` table - one row per price observation."""

    __tablename__ = "price_points"

    # TODO: define the columns for this table:
    # - `id`: an auto-incrementing integer primary key
    #   (`Column(Integer, primary_key=True, autoincrement=True)`)
    # - `bag_id`: a `String` foreign key referencing `bags.id`
    #   (`Column(String, ForeignKey("bags.id"), nullable=False)`)
    # - `price`: `Column(Float, nullable=False)`
    # - `currency`: `Column(String, nullable=False)`
    # - `timestamp`: `Column(DateTime, nullable=False)`

    # TODO: define the inverse side of the relationship:
    # `bag = relationship("BagORM", back_populates="price_history")`
