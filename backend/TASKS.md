# Task Checklist

A granular, check-the-box breakdown of every phase. Each task is small
(one method or one small piece of logic), states **what to do** and
**how you'll know it's done**. For *why* something works the way it does,
read the matching guide in [docs/](docs/) — this file is the "what's
next", the guide is the "why".

Work top to bottom. Don't skip ahead — later phases assume earlier ones
work.

## Phase 0 — Concepts (no code!)

Guide: [docs/00-concepts.md](docs/00-concepts.md)

- [ ] Read the whole primer (~15 min). It explains, from zero: what an
      API is, what CRUD means, what a database table is, and what
      Model-View-Controller is — all using this project as the example.
- [ ] Answer the 6 "Check yourself" questions at the bottom *out loud,
      in your own words*, before peeking at the answers.
- [ ] Don't worry about memorizing — every phase below links back to the
      relevant section when the concept shows up for real.

## Setup

- [ ] Install Python 3.11+ if you don't have it (`python3 --version`)
- [ ] `cd backend`
- [ ] Create a virtual environment: `python3 -m venv .venv`
- [ ] Activate it: `source .venv/bin/activate` (you'll need to do this
      every time you open a new terminal)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run `pytest -v` — you should see ~33 tests, **all failing** with
      `NotImplementedError`. That's expected — this is your starting line.

---

## Phase 1 — `app/models.py`

Guide: [docs/01-models.md](docs/01-models.md)

- [ ] Implement `Bag.add_price`: append a new `PricePoint` to
      `self.price_history`. If no `timestamp` is given, use
      `datetime.now()`.
  - Check: `pytest -v tests/test_models.py::test_add_price_and_current_price`
- [ ] Implement `Bag.current_price`: return the last item in
      `price_history`, or `None` if it's empty.
  - Check: `pytest -v tests/test_models.py::test_current_price_empty`
  - Check: `pytest -v tests/test_models.py::test_current_price_returns_most_recent`
- [ ] Implement `Bag.price_change`: return `latest.price -
      previous.price`, or `None` if there are fewer than 2 price points.
  - Check: `pytest -v tests/test_models.py -k price_change`
- [ ] Run the whole file: `pytest -v tests/test_models.py` — all 7 should
      pass.
- [ ] Concept check: answer the 2 questions at the bottom of the guide
      (you just built the **Model** in MVC).

---

## Phase 2 — `app/store.py` (part 1: CRUD + indexing)

Guide: [docs/02-store.md](docs/02-store.md)

- [ ] Implement `BagStore.add`: store the bag by id in `self._bags`,
      and append its id to `self._by_brand[bag.brand]`.
  - Tip: `self._by_brand.setdefault(bag.brand, []).append(bag.id)`
- [ ] Implement `BagStore.get`: return `self._bags.get(bag_id)`.
- [ ] Implement `BagStore.all`: return `self._bags.values()`.
  - Check so far: `pytest -v tests/test_store.py::test_all_returns_every_bag`
- [ ] Implement `BagStore.remove`: look up the bag, return `False` if
      missing; otherwise delete from both `_bags` and `_by_brand`,
      return `True`.
  - Check: `pytest -v tests/test_store.py::test_basic_crud`
- [ ] Implement `BagStore.by_brand`: map the ids in
      `_by_brand.get(brand, [])` to `Bag`s via `_bags`.
  - Check: `pytest -v tests/test_store.py::test_by_brand_index`

## Phase 3 — `app/store.py` (part 2: sorting & filtering)

Guide: [docs/02-store.md](docs/02-store.md)

- [ ] Implement `BagStore.cheapest`: filter to bags with a
      `current_price()`, then `heapq.nsmallest(n, bags, key=...)`.
  - Check: `pytest -v tests/test_store.py::test_cheapest`
- [ ] Implement `BagStore.filter_by_price_range`: list comprehension
      checking `min_price <= bag.current_price().price <= max_price`.
  - Check: `pytest -v tests/test_store.py::test_filter_by_price_range`
- [ ] Run the whole file: `pytest -v tests/test_store.py` — all 5 should
      pass.
- [ ] Concept check: answer the 3 questions at the bottom of the guide
      (you just hand-built **CRUD**).

---

## Phase 4 — `app/main.py` + `app/schemas.py`

Guide: [docs/03-api.md](docs/03-api.md)

- [ ] Read through `app/schemas.py` — no changes needed, just understand
      `BagCreate` and `BagResponse`.
- [ ] Implement `_to_response` in `main.py`: build a
      `PricePointResponse` from `bag.current_price()` (or `None`),
      then a `BagResponse`.
- [ ] Implement `list_bags`: `[_to_response(b) for b in store.all()]`.
  - Check: `pytest -v tests/test_api.py::test_list_bags_includes_created`
- [ ] Implement `cheapest_bags`: same idea using `store.cheapest(n)`.
  - Check: `pytest -v tests/test_api.py::test_cheapest_endpoint`
- [ ] Implement `get_bag`: 404 via `HTTPException` if missing, else
      `_to_response`.
  - Check: `pytest -v tests/test_api.py::test_get_missing_bag_returns_404`
- [ ] Implement `create_bag`: build a `Bag` from `payload`, call
      `add_price` if `payload.price` is set, `store.add(bag)`, return
      `_to_response(bag)`.
  - Check: `pytest -v tests/test_api.py::test_create_and_get_bag`
- [ ] Run the whole file: `pytest -v tests/test_api.py` — all 4 should
      pass.
- [ ] Manual check: `uvicorn app.main:app --reload`, then open
      `http://localhost:8000/docs` in a browser and try the endpoints.
- [ ] Concept check: answer the 4 questions at the bottom of the guide
      (you just built an **API**, with `main.py` as the **Controller**
      and `schemas.py` as the **View**).

---

## Phase 5 — `app/storage.py`

Guide: [docs/04-storage.md](docs/04-storage.md)

- [ ] Implement `save_store`: write a JSON array of bags (see the
      shape in the module docstring) to `path`.
- [ ] Implement `load_store`: read that JSON array back into a new
      `BagStore`.
  - Check: `pytest -v tests/test_storage.py::test_save_and_load_round_trip`
  - Check: `pytest -v tests/test_storage.py::test_load_sample_bags`
- [ ] (Optional) Wire `app/main.py` to call `load_store` on startup if
      `data/sample_bags.json` exists (see the `# TODO (Phase 5)`
      comment near the top of `main.py`).
- [ ] Run the whole file: `pytest -v tests/test_storage.py` — both should
      pass.

---

## Phase 5.5 — Database with Docker + SQLAlchemy

Guide: [docs/05-database.md](docs/05-database.md)

- [ ] Install Docker Desktop if you don't have it.
- [ ] `docker compose up -d` (from `backend/`) — starts a Postgres
      container.
- [ ] `docker compose ps` — confirm the `db` service is healthy.
- [ ] `cp .env.example .env`
- [ ] In `app/db_models.py`, add the columns to `PricePointORM`: `id`,
      `bag_id`, `price`, `currency`, `timestamp`.
- [ ] Add the `bag = relationship(...)` on `PricePointORM` and
      `price_history = relationship(...)` on `BagORM`.
- [ ] In `app/db.py`, implement `init_db()` (import `db_models`, then
      `Base.metadata.create_all(bind=engine)`).
- [ ] In `app/db_store.py`, implement `_to_dataclass`.
- [ ] Implement `SqlBagStore.add`.
  - Check: `pytest -v tests/test_db_store.py::test_add_and_get`
- [ ] Implement `SqlBagStore.get` and `remove`.
  - Check: `pytest -v tests/test_db_store.py::test_remove`
- [ ] Implement `SqlBagStore.all` and `by_brand`.
  - Check: `pytest -v tests/test_db_store.py::test_all_and_by_brand`
- [ ] Implement `SqlBagStore.cheapest` and `filter_by_price_range`.
  - Check: `pytest -v tests/test_db_store.py::test_cheapest`
  - Check: `pytest -v tests/test_db_store.py::test_filter_by_price_range`
- [ ] Run the whole file: `pytest -v tests/test_db_store.py` — all 6
      should pass (runs against in-memory SQLite, no Docker needed for
      this).
- [ ] Manual check: with the Postgres container running, write a small
      script that calls `init_db()` and `SqlBagStore().add(...)`, then
      inspect the data with
      `docker compose exec db psql -U postgres -d bagtracker -c "SELECT * FROM bags;"`.
- [ ] Concept check: answer the 4 questions at the bottom of the guide
      (you just built real **tables** with a foreign-key relationship —
      and saw the MVC payoff when `main.py` didn't need to change).

---

## Phase 6 — `app/scraper.py`

Guide: [docs/06-scraper.md](docs/06-scraper.md)

- [ ] Implement `fetch_raw_listings`: `httpx.get(url)`,
      `.raise_for_status()`, return `.json()`.
  - Check: `pytest -v tests/test_scraper.py::test_fetch_raw_listings`
- [ ] Implement `parse_listing`: return
      `(raw["bag_id"], raw["price"], raw["currency"])`.
  - Check: `pytest -v tests/test_scraper.py::test_parse_listing`
- [ ] Implement `fetch_and_update`: for each parsed listing, if the
      bag exists in `store`, call `add_price` and count it.
  - Check: `pytest -v tests/test_scraper.py::test_fetch_and_update`
- [ ] Run the whole file: `pytest -v tests/test_scraper.py` — all 3
      should pass.

---

## Phase 7 — `app/alerts.py`

Guide: [docs/07-alerts.md](docs/07-alerts.md)

- [ ] Implement `check_alerts`: for each `AlertRule`, look up the bag;
      skip if missing or no current price; if
      `current_price <= threshold_price`, append a `TriggeredAlert`.
  - Check: `pytest -v tests/test_alerts.py`
- [ ] All 3 tests should pass.

---

## Phase 8 — `app/agent.py`

Guide: [docs/08-agent.md](docs/08-agent.md)

- [ ] Implement `build_tools`: define the 3 tool schemas
      (`cheapest_bags`, `bags_by_brand`, `filter_by_price_range`).
  - Check: `pytest -v tests/test_agent.py::test_build_tools_has_expected_names`
- [ ] Implement `_bag_summary`: small dict with `id`, `brand`, `model`,
      `color`, `condition`, `current_price`.
- [ ] Implement `_execute_tool`: dispatch to the right `BagStore`
      method based on `name`.
- [ ] Implement `run_agent`: the tool-use loop (see the guide for the
      exact message-building steps).
  - Check: `pytest -v tests/test_agent.py::test_run_agent_executes_tool_and_returns_text`
  - Check: `pytest -v tests/test_agent.py::test_run_agent_returns_text_immediately_without_tool_use`
- [ ] Run the whole file: `pytest -v tests/test_agent.py` — all 3 should
      pass.
- [ ] (Optional, needs `ANTHROPIC_API_KEY`) Try `run_agent` for real with
      a question like "Show me all the Chanel bags" — see the "Try it
      for real" section of the guide.

---

## You're done! What's next?

- [ ] Run the full suite: `pytest -v` from `backend/` — all ~33 tests
      should pass.
- [ ] Pick a stretch goal from the bottom of
      [LearningPlan.md](../LearningPlan.md) (project-specific section).
