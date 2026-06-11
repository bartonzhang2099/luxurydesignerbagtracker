"""
Phase 5.5: SqlBagStore - the same interface as `BagStore`, backed by SQL.

Concepts: translating the in-memory operations from Phase 2-3
(`add`, `get`, `remove`, `all`, `by_brand`, `cheapest`,
`filter_by_price_range`) into database queries, and converting between ORM
objects (`BagORM`/`PricePointORM`) and your `Bag`/`PricePoint`
dataclasses.

`SqlBagStore` implements the same methods as `app.store.BagStore`,
so it can be used as a drop-in replacement anywhere a `BagStore` is
expected (e.g. in `app/main.py`).

Each method opens a short-lived `Session` via `self._session_factory()`,
does its work, and commits/closes - this is the standard SQLAlchemy
"session per operation" pattern for simple scripts/services.
"""

import heapq
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.db_models import BagORM, PricePointORM
from app.models import Bag, PricePoint


def _to_dataclass(orm_bag: BagORM) -> Bag:
    """Convert a `BagORM` (with its `price_history` relationship loaded)
    into a `Bag` dataclass.

    TODO:
    - Build `PricePoint(price=pp.price, currency=pp.currency,
      timestamp=pp.timestamp)` for each `pp` in `orm_bag.price_history`.
    - Construct and return a `Bag` with the matching scalar fields
      (`id`, `brand`, `model`, `color`, `condition`, `source`) plus
      `price_history=[...]`.
    """
    raise NotImplementedError


class SqlBagStore:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def add(self, bag: Bag) -> None:
        """Insert a bag (and its price history) into the database.

        TODO:
        - Open a session: `with self._session_factory() as session:`.
        - Build a `BagORM` from `bag`'s scalar fields.
        - For each `PricePoint` in `bag.price_history`, build a
          `PricePointORM` and append it to `orm_bag.price_history`
          (the relationship list).
        - `session.add(orm_bag)`, then `session.commit()`.
        """
        raise NotImplementedError

    def get(self, bag_id: str) -> Optional[Bag]:
        """Look up a bag by id.

        TODO:
        - Open a session.
        - `orm_bag = session.get(BagORM, bag_id)`.
        - Return `None` if not found, else `_to_dataclass(orm_bag)`.
        """
        raise NotImplementedError

    def remove(self, bag_id: str) -> bool:
        """Delete a bag (and its price history, via cascade).

        TODO:
        - Open a session, `session.get(BagORM, bag_id)`.
        - If `None`, return `False`.
        - Otherwise `session.delete(orm_bag)`, `session.commit()`,
          return `True`.
        """
        raise NotImplementedError

    def all(self) -> list[Bag]:
        """Return every bag in the database.

        TODO:
        - Open a session.
        - `orm_bags = session.execute(select(BagORM)).scalars().all()`.
        - Return `[_to_dataclass(b) for b in orm_bags]`.
        """
        raise NotImplementedError

    def by_brand(self, brand: str) -> list[Bag]:
        """Return all bags for a given brand.

        TODO:
        - Same as `all()`, but with `.where(BagORM.brand == brand)`
          added to the `select(...)`.
        """
        raise NotImplementedError

    def cheapest(self, n: int = 5) -> list[Bag]:
        """Return the `n` bags with the lowest current price.

        For this phase, fetch all bags (via `self.all()`) and reuse the
        same `heapq.nsmallest` approach from `BagStore.cheapest`
        (Phase 3) - filter out bags with no price history first.

        TODO: implement as described above.

        (Stretch goal: push this into SQL with a subquery that finds each
        bag's latest `price_points` row, then `ORDER BY price LIMIT n`.)
        """
        raise NotImplementedError

    def filter_by_price_range(self, min_price: float, max_price: float) -> list[Bag]:
        """Return bags whose current price is within [min_price, max_price].

        For this phase, fetch all bags (via `self.all()`) and filter in
        Python, same as `BagStore.filter_by_price_range`.

        TODO: implement as described above.
        """
        raise NotImplementedError
