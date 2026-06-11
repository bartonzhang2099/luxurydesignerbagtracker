"""
Phase 6 tests: run with `pytest -v tests/test_scraper.py`

Uses `respx` to mock the HTTP response, so no live network access or API
key is needed. Implement `app/scraper.py` until these pass.
"""

import respx
from httpx import Response

from app.models import Bag, BagCondition
from app.scraper import SOURCE_URL, fetch_and_update, fetch_raw_listings, parse_listing
from app.store import BagStore

MOCK_LISTINGS = [
    {"bag_id": "b1", "price": 8900.0, "currency": "USD"},
    {"bag_id": "unknown-bag", "price": 999.0, "currency": "USD"},
]


@respx.mock
def test_fetch_raw_listings():
    respx.get(SOURCE_URL).mock(return_value=Response(200, json=MOCK_LISTINGS))

    listings = fetch_raw_listings()

    assert listings == MOCK_LISTINGS


def test_parse_listing():
    bag_id, price, currency = parse_listing(
        {"bag_id": "b1", "price": 8900.0, "currency": "USD"}
    )

    assert bag_id == "b1"
    assert price == 8900.0
    assert currency == "USD"


@respx.mock
def test_fetch_and_update():
    respx.get(SOURCE_URL).mock(return_value=Response(200, json=MOCK_LISTINGS))

    store = BagStore()
    bag = Bag(
        id="b1",
        brand="Chanel",
        model="Classic Flap Medium",
        color="Black",
        condition=BagCondition.LIKE_NEW,
        source="test",
    )
    bag.add_price(9500.0, "USD")
    store.add(bag)

    updated_count = fetch_and_update(store)

    # Only "b1" exists in the store; "unknown-bag" should be ignored.
    assert updated_count == 1

    updated_bag = store.get("b1")
    assert updated_bag.current_price().price == 8900.0
    assert len(updated_bag.price_history) == 2
