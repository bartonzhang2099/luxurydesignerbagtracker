"""
Phase 5.5 tests: run with `pytest -v tests/test_db_store.py`

Uses an in-memory SQLite database (via a `StaticPool` so all sessions
share the same in-memory connection), so these tests don't require Docker
or Postgres. Implement `app/db_models.py` and `app/db_store.py` until
these pass - then try the real Postgres container with
`docker compose up -d` and `DATABASE_URL` pointed at it.
"""

from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.db_store import SqlBagStore
from app.models import Bag, BagCondition


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def store(session_factory):
    return SqlBagStore(session_factory=session_factory)


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
        bag.add_price(price, "USD", timestamp=datetime(2026, 1, 1, 9, 0, 0))
    return bag


def test_add_and_get(store):
    bag = make_bag("b1", "Chanel", price=9500)
    store.add(bag)

    fetched = store.get("b1")
    assert fetched is not None
    assert fetched.id == "b1"
    assert fetched.brand == "Chanel"
    assert fetched.condition == BagCondition.LIKE_NEW
    assert len(fetched.price_history) == 1
    assert fetched.current_price().price == 9500.0

    assert store.get("missing") is None


def test_remove(store):
    store.add(make_bag("b1", "Chanel", price=9500))

    assert store.remove("b1") is True
    assert store.get("b1") is None
    assert store.remove("b1") is False


def test_all_and_by_brand(store):
    store.add(make_bag("b1", "Chanel", price=9500))
    store.add(make_bag("b2", "Chanel", price=11000))
    store.add(make_bag("b3", "Louis Vuitton", price=2100))

    assert {b.id for b in store.all()} == {"b1", "b2", "b3"}

    chanel_bags = store.by_brand("Chanel")
    assert {b.id for b in chanel_bags} == {"b1", "b2"}
    assert store.by_brand("Hermès") == []


def test_cheapest(store):
    store.add(make_bag("expensive", "Hermès", price=22000))
    store.add(make_bag("cheap", "Coach", price=350))
    store.add(make_bag("medium", "Louis Vuitton", price=2100))
    store.add(make_bag("no_price", "Chanel"))

    cheapest_two = store.cheapest(2)
    assert [b.id for b in cheapest_two] == ["cheap", "medium"]


def test_filter_by_price_range(store):
    store.add(make_bag("low", "Coach", price=350))
    store.add(make_bag("mid", "Louis Vuitton", price=2100))
    store.add(make_bag("high", "Hermès", price=22000))

    in_range = store.filter_by_price_range(1000, 5000)
    assert {b.id for b in in_range} == {"mid"}


def test_price_history_order_preserved(store):
    bag = make_bag("b1", "Chanel")
    bag.add_price(9500.0, "USD", timestamp=datetime(2026, 1, 1))
    bag.add_price(8900.0, "USD", timestamp=datetime(2026, 2, 1))
    store.add(bag)

    fetched = store.get("b1")
    prices = [pp.price for pp in fetched.price_history]
    assert prices == [9500.0, 8900.0]
    assert fetched.current_price().price == 8900.0
