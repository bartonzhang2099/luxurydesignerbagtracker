# Phase 7 Guide — Price Alerts

**File to edit:** `app/alerts.py`
**Tests:** `pytest -v tests/test_alerts.py`

## Why this phase matters

This phase is intentionally small — it's a chance to practice combining
everything from Phases 1-3 (bags, stores, current price) into a small
piece of business logic, and to introduce **queues** as a data structure
for "things to process in order". The feature itself is the heart of any
price tracker: *"tell me when the Classic Flap drops below $8,000."*

## Concepts

- **`collections.deque`**: a double-ended queue — efficient `append()` and
  `popleft()` (unlike a `list`, where `pop(0)` is O(n)). Read:
  [Python docs — deque](https://docs.python.org/3/library/collections.html#collections.deque).
  Here, `check_alerts` returns a `deque` of triggered alerts that a caller
  could process one at a time with `popleft()` (e.g. "send the next
  notification").
- **Threshold logic**: a rule "fires" when `current_price <=
  threshold_price`. Note the `<=` — exactly-at-threshold should trigger
  (see `test_check_alerts_triggers_at_exact_threshold`).

## Step-by-step

1. Create an empty `deque()`.
2. For each `rule` in `rules`:
   - `bag = store.get(rule.bag_id)` — skip if `None`.
   - `price_point = bag.current_price()` — skip if `None`.
   - If `price_point.price <= rule.threshold_price`, append a
     `TriggeredAlert(bag_id=..., threshold_price=..., current_price=...)`.
3. Return the deque.

## Common pitfalls

- Using `<` instead of `<=` — the exact-threshold test will fail.
- Crashing on a bag id that doesn't exist in the store, or a bag with no
  price history — both should be silently skipped, not raise.

## Check your work

```bash
pytest -v tests/test_alerts.py
```

All 3 tests should pass before moving on to [Phase 8](08-agent.md), the
AI agent integration.
