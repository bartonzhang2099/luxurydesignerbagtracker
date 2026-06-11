"""
Phase 2 & 3: BagStore - an in-memory index over `Bag` objects.

Concepts:
- Phase 2: dictionaries for O(1) lookup, secondary indexes, lists.
- Phase 3: heaps (`heapq`) for "top N" queries, filtering with comprehensions.

Why a secondary index? `by_brand` could be implemented by scanning every
bag every time (O(n)), but maintaining a `brand -> [bag_ids]` dict
lets us answer that query in O(k) where k is the number of bags for that
brand - a classic space/time tradeoff.
"""

import heapq
from typing import Iterable, Optional

from app.models import Bag


class BagStore:
    """In-memory store of bags, indexed by id and by brand."""

    def __init__(self) -> None:
        # Primary index: bag id -> Bag
        self._bags: dict[str, Bag] = {}
        # Secondary index: brand name -> list of bag ids
        self._by_brand: dict[str, list[str]] = {}

    def add(self, bag: Bag) -> None:
        """Add a bag to the store, updating both indexes.

        TODO:
        - Store the bag in `self._bags` keyed by `bag.id`.
        - Append `bag.id` to `self._by_brand[bag.brand]`,
          creating the list if it doesn't exist yet.
        """
        raise NotImplementedError

    def get(self, bag_id: str) -> Optional[Bag]:
        """Return the bag with the given id, or None if not found.

        TODO: O(1) dict lookup, returning None if missing.
        """
        raise NotImplementedError

    def remove(self, bag_id: str) -> bool:
        """Remove a bag from the store.

        Returns True if a bag was removed, False if no bag with
        that id existed.

        TODO:
        - Look up the bag; if missing, return False.
        - Remove it from `self._bags`.
        - Remove its id from `self._by_brand[bag.brand]` (and clean up
          the list/key if it becomes empty - not required but good practice).
        - Return True.
        """
        raise NotImplementedError

    def all(self) -> Iterable[Bag]:
        """Return an iterable of every bag in the store.

        TODO: return `self._bags.values()` (or similar).
        """
        raise NotImplementedError

    def by_brand(self, brand: str) -> list[Bag]:
        """Return all bags for a given brand, using the secondary index.

        TODO:
        - Look up the list of bag ids in `self._by_brand`.
        - Map each id to its `Bag` via `self._bags`.
        - Return an empty list if the brand isn't found.
        """
        raise NotImplementedError

    def cheapest(self, n: int = 5) -> list[Bag]:
        """Return the `n` bags with the lowest current price.

        Bags with no price history should be excluded.

        TODO:
        - Build a list of bags that have a `current_price()`.
        - Use `heapq.nsmallest(n, bags, key=...)` to find the cheapest,
          keyed by `bag.current_price().price`.
        """
        raise NotImplementedError

    def filter_by_price_range(self, min_price: float, max_price: float) -> list[Bag]:
        """Return all bags whose current price is within [min_price, max_price].

        Bags with no price history should be excluded.

        TODO: use a list comprehension over `self.all()`.
        """
        raise NotImplementedError
