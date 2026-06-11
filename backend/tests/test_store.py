"""
Phase 2 & 3 tests: run with `pytest -v tests/test_store.py`

Implement `app/store.py` until all of these pass. `Bag.add_price` and
`Bag.current_price` from Phase 1 must already be working.
"""

from app.models import Bag, BagCondition
from app.store import BagStore


def make_bag(id: str, brand: str, price: float | None = None) -> Bag:
    bag = Bag(
        id=id,
        brand=brand,
        model="Some Model",
        color="Black",
        condition=BagCondition.LIKE_NEW,
        source="test",
    )
    if price is not None:
        bag.add_price(price, "USD")
    return bag


def test_basic_crud():
    store = BagStore()
    bag = make_bag("b1", "Chanel", price=9500)

    store.add(bag)
    assert store.get("b1") is bag
    assert store.get("missing") is None

    assert store.remove("b1") is True
    assert store.get("b1") is None
    assert store.remove("b1") is False


def test_all_returns_every_bag():
    store = BagStore()
    b1 = make_bag("b1", "Chanel", price=9500)
    b2 = make_bag("b2", "Louis Vuitton", price=2100)

    store.add(b1)
    store.add(b2)

    assert {b.id for b in store.all()} == {"b1", "b2"}


def test_by_brand_index():
    store = BagStore()
    b1 = make_bag("b1", "Chanel", price=9500)
    b2 = make_bag("b2", "Chanel", price=11000)
    b3 = make_bag("b3", "Louis Vuitton", price=2100)

    store.add(b1)
    store.add(b2)
    store.add(b3)

    chanel_bags = store.by_brand("Chanel")
    assert {b.id for b in chanel_bags} == {"b1", "b2"}

    assert store.by_brand("Hermès") == []


def test_cheapest():
    store = BagStore()
    store.add(make_bag("expensive", "Hermès", price=22000))
    store.add(make_bag("cheap", "Coach", price=350))
    store.add(make_bag("medium", "Louis Vuitton", price=2100))
    store.add(make_bag("no_price", "Chanel"))  # no price history

    cheapest_two = store.cheapest(2)
    assert [b.id for b in cheapest_two] == ["cheap", "medium"]


def test_filter_by_price_range():
    store = BagStore()
    store.add(make_bag("low", "Coach", price=350))
    store.add(make_bag("mid", "Louis Vuitton", price=2100))
    store.add(make_bag("high", "Hermès", price=22000))
    store.add(make_bag("no_price", "Chanel"))

    in_range = store.filter_by_price_range(1000, 5000)
    assert {b.id for b in in_range} == {"mid"}
