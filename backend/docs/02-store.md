# Phase 2 & 3 Guide — BagStore

**File to edit:** `app/store.py`
**Tests:** `pytest -v tests/test_store.py`

> **Where this fits:** `add` / `get` / `remove` / `all` is your first
> [CRUD](00-concepts.md#2-what-is-crud) — Create, Read, Update, Delete —
> implemented by hand with dictionaries. In Phase 4 you'll expose this
> exact CRUD over an API; in Phase 5.5 you'll re-implement it on a real
> database. Same four verbs every time.

## Why this phase matters

This is the core data structures phase. You'll build an in-memory database
of bags using nothing but dicts, lists, and `heapq` — the same
fundamentals that power real databases' indexes.

## Concepts

### Phase 2: Hash maps & secondary indexes

- A Python `dict` gives **O(1) average-case lookup** by key. `_bags:
  dict[str, Bag]` lets `get(bag_id)` be instant regardless of how many
  bags exist.
- A **secondary index** (`_by_brand: dict[str, list[str]]`) trades memory
  and write-time bookkeeping for fast reads. Every time you `add()` a
  bag, you update *both* structures so they stay in sync. This is the
  same idea behind database indexes — and the same tradeoff (writes get
  slightly slower, reads get much faster).

### Phase 3: Heaps & filtering

- `heapq.nsmallest(n, iterable, key=...)` finds the `n` smallest items
  without fully sorting the list — useful when `n` is small relative to
  the total. Read:
  [Python docs — heapq](https://docs.python.org/3/library/heapq.html#heapq.nsmallest).
- `key=` is a function applied to each item to get the value to compare —
  here, you'll want `lambda b: b.current_price().price`.
- Filtering with a list comprehension: `[b for b in store.all() if ...]`.

## Step-by-step

1. **`add`**: two writes — `self._bags[bag.id] = bag`, then append
   `bag.id` to `self._by_brand[bag.brand]` (use
   `dict.setdefault(bag.brand, [])` to handle the first bag for a
   brand).
2. **`get`**: one line, `self._bags.get(bag_id)`.
3. **`remove`**: look up the bag first (need its `.brand` to clean the
   secondary index), then delete from both structures.
4. **`all`**: `self._bags.values()`.
5. **`by_brand`**: get the list of ids from `_by_brand`, then map to
   `Bag`s via `_bags`. Handle the "brand not found" case (return `[]`,
   don't raise).
6. **`cheapest`**: filter to bags with a `current_price()`, then
   `heapq.nsmallest`.
7. **`filter_by_price_range`**: same filtering idea, but with a range
   check instead of a heap.

## Common pitfalls

- Forgetting to exclude bags with no price history in `cheapest` and
  `filter_by_price_range` — calling `.price` on `None` will crash.
- Not keeping `_bags` and `_by_brand` in sync on `remove` — leads to
  "ghost" ids in the secondary index.

## Check your work

```bash
pytest -v tests/test_store.py
```

All 5 tests should pass before moving on to [Phase 4](03-api.md).

## Concept check (say it out loud)

1. Which method is the C in CRUD? The R? The D? Where did U go?
   (Hint: look back at `Bag.add_price` from Phase 1.)
2. `_bags` is keyed by id, like a table's *primary key*. What plays
   that role, and what would break if two bags shared an id?
3. The `_by_brand` secondary index makes reads faster but writes slower.
   When is that trade worth it?
