"""
Phase 5: JSON persistence for a `BagStore`.

Concepts: serialization, file I/O, round-tripping objects through a plain
data format (dicts/lists/strings) that JSON can represent.

Datetimes and enums aren't natively JSON-serializable, so they need to be
converted to/from strings (`datetime.isoformat()` / `BagCondition.value`).

JSON shape for a single bag:

```json
{
  "id": "chanel-flap-001",
  "brand": "Chanel",
  "model": "Classic Flap Medium",
  "color": "Black",
  "condition": "like_new",
  "source": "example",
  "price_history": [
    {"price": 9500.0, "currency": "USD", "timestamp": "2026-01-01T12:00:00"}
  ]
}
```

The file as a whole is a JSON array of these bag objects.
"""

import json
from datetime import datetime
from pathlib import Path

from app.models import Bag, BagCondition, PricePoint
from app.store import BagStore


def save_store(store: BagStore, path: Path) -> None:
    """Write every bag in `store` to `path` as a JSON array.

    TODO:
    - Build a list of dicts, one per bag (see module docstring for shape).
      - Each `price_history[*].timestamp` should be an `.isoformat()`
        string.
      - `condition` should be `.value` (a plain string).
    - Write the list to `path` with `json.dump` (consider `indent=2` for
      readability).
    """
    raise NotImplementedError


def load_store(path: Path) -> BagStore:
    """Read a JSON array from `path` and return a populated `BagStore`.

    TODO:
    - Read and `json.load` the file at `path`.
    - For each bag dict:
      - Parse `condition` with `BagCondition(...)`.
      - Build the `Bag`, then for each entry in `price_history`,
        construct a `PricePoint` (parsing its `timestamp` with
        `datetime.fromisoformat(...)`) and append it to
        `bag.price_history` directly (or use `add_price`).
    - Add each `Bag` to a new `BagStore` and return it.
    """
    raise NotImplementedError
