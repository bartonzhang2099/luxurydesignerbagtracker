# Phase 6 Guide — Fetching Real Bag Price Data

**File to edit:** `app/scraper.py`
**Tests:** `pytest -v tests/test_scraper.py`

## Why this phase matters

This is your first interaction with the outside world: making HTTP
requests, handling responses (and failures), and translating someone
else's data shape into your own models. This pattern — fetch, parse,
update — is the core of almost any data-pipeline or integration code.
It's also literally what price-tracking sites do: periodically re-check
listings and record the new prices.

## Concepts

- **`httpx.get(url)`**: makes a synchronous HTTP GET request and returns a
  `Response`. Read:
  [httpx Quickstart](https://www.python-httpx.org/quickstart/).
- **`response.raise_for_status()`**: raises an exception if the response
  was a 4xx/5xx error — fail loudly instead of silently processing bad
  data.
- **`response.json()`**: parses the response body as JSON into Python
  lists/dicts.
- **Mocking HTTP in tests**: `tests/test_scraper.py` uses `respx` to
  intercept requests to `SOURCE_URL` and return canned responses, so your
  tests are fast and don't depend on a real server. Read:
  [respx docs](https://lundberg.github.io/respx/).

## Step-by-step

1. **`fetch_raw_listings`**: `httpx.get(url)`, `.raise_for_status()`,
   return `.json()`. Three lines.
2. **`parse_listing`**: pull `bag_id`, `price`, `currency` out of the
   raw dict and return them as a tuple. This is intentionally simple —
   the "mapping" logic.
3. **`fetch_and_update`**: tie it together —
   ```python
   count = 0
   for raw in fetch_raw_listings(url):
       bag_id, price, currency = parse_listing(raw)
       bag = store.get(bag_id)
       if bag is not None:
           bag.add_price(price, currency)
           count += 1
   return count
   ```

## Common pitfalls

- Tests mock `SOURCE_URL` exactly — if you hardcode a different URL in
  `fetch_raw_listings`'s default argument, the mock won't match. Always
  default to the `SOURCE_URL` constant.
- Listings for bags that don't exist in the store should be **skipped
  silently**, not raise an error (`test_fetch_and_update` checks this via
  `"unknown-bag"`).

## Going further (optional, real data)

Set the `SOURCE_URL` environment variable to point at a real source —
e.g. a resale marketplace API or feed you have access to — matching the
`{"bag_id": ..., "price": ..., "currency": ...}` shape (or adjust
`parse_listing` to match whatever shape the real source returns).

```bash
export SOURCE_URL="https://api.example.com/bags"
```

## Check your work

```bash
pytest -v tests/test_scraper.py
```

All 3 tests should pass before moving on to [Phase 7](07-alerts.md).
