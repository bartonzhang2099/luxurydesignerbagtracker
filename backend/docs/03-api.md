# Phase 4 Guide — Backend API

**Files to edit:** `app/schemas.py`, `app/main.py`
**Tests:** `pytest -v tests/test_api.py`

> **Where this fits:** this phase builds the
> [API](00-concepts.md#1-what-is-a-backend-what-is-an-api) — the menu the
> outside world orders from. In MVC terms, `main.py`'s route functions
> are the **Controller** (receive request → call model → return
> response) and `schemas.py` is the **View** (the JSON shape that goes
> out). And each endpoint is one [CRUD](00-concepts.md#2-what-is-crud)
> verb over HTTP: `POST /bags` = Create, `GET /bags` = Read.

## Why this phase matters

This is where your data structures become a real, callable web service.
You'll learn the request/response cycle that almost every backend job
requires: validate input, query your data layer, shape the output.

## Concepts

- **Pydantic models** (`app/schemas.py`) describe the *shape* of data
  crossing the API boundary, separate from your internal `Bag`
  dataclass. FastAPI uses them to validate incoming JSON and to generate
  response JSON automatically. Read:
  [FastAPI — Request Body](https://fastapi.tiangolo.com/tutorial/body/) and
  [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
- **Path params vs. query params**: `/bags/{bag_id}` is a path param
  (part of the URL); `?n=5` in `/bags/cheapest?n=5` is a query param (a
  function argument with a default value).
- **`HTTPException`**: how you return non-200 responses (e.g. 404) from a
  route handler.
- **Route ordering matters**: FastAPI matches routes top-to-bottom.
  `/bags/cheapest` must be declared *before* `/bags/{bag_id}`, or
  `"cheapest"` gets captured as a `bag_id` and you'll get a 404 (or a
  422 if it fails to parse).

## Step-by-step

1. In `schemas.py`, the Pydantic models are mostly given to you — read
   through `BagCreate` and `BagResponse` and make sure you understand
   what each field maps to.
2. In `main.py`, start with `_to_response`: this is a pure conversion
   function (`Bag` -> `BagResponse`). Get `bag.current_price()`, convert
   it to a `PricePointResponse` if present, then build the `BagResponse`.
3. `list_bags`: one line using `_to_response` and `store.all()`.
4. `cheapest_bags`: same idea with `store.cheapest(n)`.
5. `get_bag`: look up, raise `HTTPException(404, ...)` if missing, else
   convert and return.
6. `create_bag`: construct a `Bag` from `payload`'s fields (note
   `payload` is a `BagCreate`, which has extra `price`/`currency` fields
   not on `Bag` itself — don't pass those to `Bag(...)` directly). Add
   an initial price if `payload.price` is set, then `store.add(bag)`.

## Common pitfalls

- Passing `payload.price` / `payload.currency` into `Bag(...)` — they
  aren't fields on `Bag`. Use `bag.add_price(...)` instead.
- Route order (see above) — if `/bags/cheapest` 404s or errors with
  "value is not a valid... bag_id", check route order first.
- `BagCreate.condition` is a `BagCondition` enum (Pydantic will validate
  the incoming string against it automatically) — pass it straight
  through to `Bag(condition=payload.condition, ...)`.

## Try it manually

```bash
uvicorn app.main:app --reload
# in another terminal:
curl -X POST localhost:8000/bags -H 'Content-Type: application/json' -d '{
  "id": "b1", "brand": "Chanel", "model": "Classic Flap Medium",
  "color": "Black", "condition": "like_new",
  "source": "manual", "price": 9500, "currency": "USD"
}'
curl localhost:8000/bags
curl localhost:8000/bags/cheapest?n=1
```

Or open `http://localhost:8000/docs` for FastAPI's auto-generated
interactive API explorer.

## Check your work

```bash
pytest -v tests/test_api.py
```

All 4 tests should pass before moving on to [Phase 5](04-storage.md).

## Concept check (say it out loud)

1. Walk through the six steps of
   [how a request flows](00-concepts.md#5-how-a-request-actually-flows-tying-it-together)
   for `GET /bags/cheapest?n=2`, naming the actual functions in this
   repo at each step.
2. Why do `Bag` (the model) and `BagResponse` (the view) both exist?
   What could you change in one without touching the other?
3. Why is "bag not found" a `404` response rather than a Python
   exception crashing the server?
4. Which CRUD operations does the API *not* expose yet? Sketch (on
   paper) what `DELETE /bags/{id}` would look like.
