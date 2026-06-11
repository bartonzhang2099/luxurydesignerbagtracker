"""
Phase 7 tests: run with `pytest -v tests/test_alerts.py`

Implement `app/alerts.py` until these pass.
"""

from app.alerts import AlertRule, check_alerts
from app.models import Bag, BagCondition
from app.store import BagStore


def make_bag(id: str, price: float | None = None) -> Bag:
    bag = Bag(
        id=id,
        brand="Chanel",
        model="Classic Flap Medium",
        color="Black",
        condition=BagCondition.LIKE_NEW,
        source="test",
    )
    if price is not None:
        bag.add_price(price, "USD")
    return bag


def test_check_alerts_triggers_when_at_or_below_threshold():
    store = BagStore()
    store.add(make_bag("b1", price=7800.0))
    store.add(make_bag("b2", price=9500.0))

    rules = [
        AlertRule(bag_id="b1", threshold_price=8000.0),  # should trigger
        AlertRule(bag_id="b2", threshold_price=9000.0),  # should not trigger
    ]

    triggered = check_alerts(store, rules)

    assert len(triggered) == 1
    alert = triggered[0]
    assert alert.bag_id == "b1"
    assert alert.current_price == 7800.0
    assert alert.threshold_price == 8000.0


def test_check_alerts_ignores_missing_or_priceless_bags():
    store = BagStore()
    store.add(make_bag("b1"))  # no price history

    rules = [
        AlertRule(bag_id="b1", threshold_price=1000.0),
        AlertRule(bag_id="missing", threshold_price=1000.0),
    ]

    triggered = check_alerts(store, rules)

    assert len(triggered) == 0


def test_check_alerts_triggers_at_exact_threshold():
    store = BagStore()
    store.add(make_bag("b1", price=8000.0))

    rules = [AlertRule(bag_id="b1", threshold_price=8000.0)]

    triggered = check_alerts(store, rules)

    assert len(triggered) == 1
