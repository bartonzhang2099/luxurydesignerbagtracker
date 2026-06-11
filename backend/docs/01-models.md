# Phase 1 Guide — Modeling a Bag

**File to edit:** `app/models.py`
**Tests:** `pytest -v tests/test_models.py`

> **Where this fits:** this is the **Model** in
> [Model-View-Controller](00-concepts.md#4-what-is-mvc-model-view-controller) —
> *what the data is and what it can do*. Notice it imports nothing about
> the web, files, or databases. That's on purpose.

## Why this phase matters

Every later phase builds on these two classes. `Bag` and `PricePoint`
are the "nouns" of this project — get comfortable with them now and
everything else (storage, API, agent) is just operating on them.

## Concepts

- **`@dataclass`**: a decorator that auto-generates `__init__`, `__repr__`,
  and `__eq__` for a class based on its annotated fields. Read:
  [Python docs — dataclasses](https://docs.python.org/3/library/dataclasses.html).
- **`Enum`**: a fixed set of named constants (here, bag conditions).
  `class BagCondition(str, Enum)` makes each member behave like a string,
  which is handy for JSON serialization later.
- **`Optional[T]`**: shorthand for `T | None` — a value that might be
  missing.
- **`field(default_factory=list)`**: how you give a dataclass field a
  mutable default (you can't write `price_history: list = []` directly —
  Python would share that one list across every instance).

## Step-by-step

1. Start with `Bag.add_price`. It's the simplest: construct a
   `PricePoint` and append it to `self.price_history`. Remember the
   default timestamp (`datetime.now()`) when none is given.
2. `Bag.current_price`: think about what "most recent" means for a list
   that's appended to in chronological order. What's the simplest way to
   get the last element? What if the list is empty?
3. `Bag.price_change`: you need the *last two* price points. How do you
   slice the last two elements of a list? What should happen if there's
   only zero or one price point?

## Common pitfalls

- Forgetting to handle the empty/short list cases (tests check these
  explicitly).
- Using `datetime.now()` as a *default argument value* (`def add_price(...,
  timestamp=datetime.now())`) — this evaluates once at import time, not
  per-call. Use `Optional[datetime] = None` and check inside the function
  instead.

## Check your work

```bash
pytest -v tests/test_models.py
```

All 7 tests should pass before moving on to
[Phase 2](02-store.md).

## Concept check (say it out loud)

1. Why does `models.py` know nothing about HTTP or databases — what's
   the benefit of keeping the Model "pure"?
2. `Bag` *is* data but also *has behavior* (`current_price`). Why put
   that method here instead of wherever it's needed later?
