# Phase 5 Guide — JSON Persistence

**File to edit:** `app/storage.py`
**Tests:** `pytest -v tests/test_storage.py`

## Why this phase matters

Right now, every bag lives in memory and disappears when the server
restarts. This phase teaches **serialization** — converting your Python
objects into a format (JSON) that can be written to disk and read back,
which is the foundation of every database driver and API client you'll
ever use.

## Concepts

- **JSON can't represent everything**: `datetime` and `Enum` objects need
  to be converted to plain strings before `json.dump` will accept them,
  and converted back after `json.load`.
  - `datetime.isoformat()` -> string, `datetime.fromisoformat(s)` -> back.
  - `BagCondition.LIKE_NEW.value` -> `"like_new"`,
    `BagCondition("like_new")` -> back to the enum member.
- **Round-tripping**: "save then load should give you equivalent data" is
  a powerful way to test serialization code — see
  `test_save_and_load_round_trip`.

## Step-by-step

1. Look at the JSON shape documented in the `app/storage.py` module
   docstring — that's the contract both functions need to agree on.
2. **`save_store`**: for each `bag in store.all()`, build a dict with
   the bag's scalar fields plus a `price_history` list of dicts (one
   per `PricePoint`). Write the whole list with `json.dump(data, f,
   indent=2)`.
3. **`load_store`**: `json.load` the file, then for each bag dict,
   reverse the conversions — parse each price point's `timestamp` with
   `datetime.fromisoformat`, parse `condition` with `BagCondition(...)`.
   Build a `Bag`, manually append `PricePoint`s to `bag.price_history`
   (in order!), then `store.add(bag)`.

## Common pitfalls

- `Path` objects need `open(path, "w")` / `open(path)` —
  `json.dump`/`json.load` work on file objects, not paths directly.
- Losing price history order — `price_history` is meant to stay oldest
  -> newest, since `current_price()` relies on that.
- Mismatched enum values — `BagCondition("like_new")` (constructor call)
  looks up by *value*, not by name (`BagCondition["LIKE_NEW"]` would
  look up by name — different syntax, don't mix them up).

## Try it manually

Once both functions work, wire `app/main.py` to load
`data/sample_bags.json` on startup (there's a `# TODO (Phase 5)` comment
marking where) so the API starts with real-looking data:

```python
from pathlib import Path
from app.storage import load_store

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_bags.json"
if DATA_PATH.exists():
    store = load_store(DATA_PATH)
```

## Check your work

```bash
pytest -v tests/test_storage.py
```

Both tests should pass before moving on to [Phase 5.5](05-database.md), a
detour into running a real database locally with Docker.
