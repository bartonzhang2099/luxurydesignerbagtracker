"""
Phase 6: Fetching real(ish) bag price data over HTTP.

Concepts: HTTP clients (`httpx`), error handling, mapping external data
into your own models, and writing tests against mocked HTTP responses
(see `tests/test_scraper.py`, which uses `respx`).

`SOURCE_URL` is read from the environment so the same code can point at a
mock server during development/tests and a real source later (e.g. a
resale marketplace's API or feed).

Expected raw listing shape (a list of these is returned by the source):

```json
{"bag_id": "chanel-flap-001", "price": 9200.0, "currency": "USD"}
```
"""

import os

import httpx

from app.store import BagStore

SOURCE_URL = os.environ.get("SOURCE_URL", "https://example.com/api/bags")


def fetch_raw_listings(url: str = SOURCE_URL) -> list[dict]:
    """Fetch raw bag listings from `url`.

    TODO:
    - Make a GET request to `url` with `httpx.get(...)`.
    - Call `.raise_for_status()` so HTTP errors raise an exception.
    - Return `.json()` (expected to be a list of dicts).
    """
    raise NotImplementedError


def parse_listing(raw: dict) -> tuple[str, float, str]:
    """Extract `(bag_id, price, currency)` from a raw listing dict.

    TODO:
    - Return `(raw["bag_id"], raw["price"], raw["currency"])`.
    - (Optional) handle missing/malformed fields gracefully.
    """
    raise NotImplementedError


def fetch_and_update(store: BagStore, url: str = SOURCE_URL) -> int:
    """Fetch listings and record a new price for each matching bag.

    Returns the number of bags updated.

    TODO:
    - Call `fetch_raw_listings(url)`.
    - For each raw listing, call `parse_listing` to get
      `(bag_id, price, currency)`.
    - Look up the bag in `store`. If found, call
      `bag.add_price(price, currency)` and increment a counter.
    - Return the counter.
    """
    raise NotImplementedError
