"""
Phase 1 tests: run with `pytest -v tests/test_models.py`

These tests describe the expected behavior of `Bag` and `PricePoint`
before you've implemented them. Implement the methods in
`app/models.py` until all of these pass.
"""

from datetime import datetime, timedelta

from app.models import Bag, BagCondition


def make_bag() -> Bag:
    return Bag(
        id="b1",
        brand="Chanel",
        model="Classic Flap Medium",
        color="Black",
        condition=BagCondition.LIKE_NEW,
        source="test",
    )


def test_current_price_empty():
    bag = make_bag()
    assert bag.current_price() is None


def test_add_price_and_current_price():
    bag = make_bag()
    now = datetime(2026, 1, 1, 12, 0, 0)

    bag.add_price(9500.0, "USD", timestamp=now)

    current = bag.current_price()
    assert current is not None
    assert current.price == 9500.0
    assert current.currency == "USD"
    assert current.timestamp == now


def test_add_price_defaults_timestamp():
    bag = make_bag()
    before = datetime.now()

    bag.add_price(9500.0, "USD")

    after = datetime.now()
    current = bag.current_price()
    assert current is not None
    assert before <= current.timestamp <= after


def test_current_price_returns_most_recent():
    bag = make_bag()
    t1 = datetime(2026, 1, 1)
    t2 = t1 + timedelta(days=1)

    bag.add_price(9500.0, "USD", timestamp=t1)
    bag.add_price(8900.0, "USD", timestamp=t2)

    current = bag.current_price()
    assert current is not None
    assert current.price == 8900.0
    assert current.timestamp == t2


def test_price_change_with_no_history():
    bag = make_bag()
    assert bag.price_change() is None


def test_price_change_with_one_price():
    bag = make_bag()
    bag.add_price(9500.0, "USD")
    assert bag.price_change() is None


def test_price_change_with_multiple_prices():
    bag = make_bag()
    bag.add_price(9500.0, "USD", timestamp=datetime(2026, 1, 1))
    bag.add_price(8900.0, "USD", timestamp=datetime(2026, 1, 2))

    assert bag.price_change() == -600.0
