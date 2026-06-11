"""
Phase 7: Price alerts.

Concepts: simple threshold logic, modeling "rules" as data, queues
(`collections.deque`) for ordered pending work.

Think: "tell me when the Chanel Classic Flap drops below $8,000."
"""

from collections import deque
from dataclasses import dataclass

from app.store import BagStore


@dataclass
class AlertRule:
    """A rule that triggers when a bag's current price drops to or
    below `threshold_price`."""

    bag_id: str
    threshold_price: float


@dataclass
class TriggeredAlert:
    """An alert that fired because its rule's condition was met."""

    bag_id: str
    threshold_price: float
    current_price: float


def check_alerts(store: BagStore, rules: list[AlertRule]) -> deque[TriggeredAlert]:
    """Check each rule against the store and return triggered alerts.

    A rule triggers if the bag exists, has a current price, and that
    price is <= `rule.threshold_price`.

    Returns a `deque` of `TriggeredAlert`s in the same order as `rules`,
    so callers can process them as a queue (e.g. `popleft()` to send
    notifications one at a time).

    TODO:
    - For each rule in `rules`:
      - Look up the bag via `store.get(rule.bag_id)`.
      - Skip if the bag doesn't exist or has no `current_price()`.
      - If `current_price().price <= rule.threshold_price`, append a
        `TriggeredAlert` to the result deque.
    - Return the deque.
    """
    raise NotImplementedError
