"""
Phase 1: Core data models.

Concepts: dataclasses, enums, type hints, methods on data objects.

You'll model a single bag listing (`Bag`) and its price history
(`PricePoint`). These are the building blocks every later phase depends on.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class BagCondition(str, Enum):
    """Condition of a listed bag.

    Using `str, Enum` lets these values serialize to/from JSON cleanly
    (e.g. for the API responses in Phase 4 and storage in Phase 5).
    """

    NEW = "new"
    LIKE_NEW = "like_new"
    GENTLY_USED = "gently_used"
    VINTAGE = "vintage"


@dataclass
class PricePoint:
    """A single price observation for a bag at a point in time."""

    price: float
    currency: str
    timestamp: datetime


@dataclass
class Bag:
    """A single bag listing tracked over time.

    `price_history` holds every `PricePoint` ever observed for this
    bag, oldest first.
    """

    id: str
    brand: str  # e.g. "Chanel", "Hermès", "Louis Vuitton"
    model: str  # e.g. "Classic Flap Medium", "Birkin 25"
    color: str
    condition: BagCondition
    source: str  # where the listing lives, e.g. "Fashionphile"
    price_history: list[PricePoint] = field(default_factory=list)

    def add_price(
        self, price: float, currency: str, timestamp: Optional[datetime] = None
    ) -> None:
        """Record a new price observation.

        TODO:
        - If `timestamp` is None, default to `datetime.now()`.
        - Append a new `PricePoint` to `self.price_history`.
        """
        raise NotImplementedError

    def current_price(self) -> Optional[PricePoint]:
        """Return the most recent `PricePoint`, or `None` if there's no history.

        TODO:
        - Return `None` if `price_history` is empty.
        - Otherwise return the last element of `price_history`.
          (Hint: price_history is ordered oldest -> newest.)
        """
        raise NotImplementedError

    def price_change(self) -> Optional[float]:
        """Return the change from the previous price to the current price.

        e.g. if the last two prices were 5000 then 4500, this returns -500.

        TODO:
        - Return `None` if there are fewer than 2 price points.
        - Otherwise return `latest.price - previous.price`.
        """
        raise NotImplementedError
