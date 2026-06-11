# CLAUDE.md

## What this repo is

A **teaching repo**, not a normal codebase. It's a guided curriculum for a
complete beginner (the owner's girlfriend) to learn backend development by
building a luxury designer bag price tracker (Chanel, Hermès, LV resale
prices over time). The owner mentors via PRs; the learner implements the
skeletons phase by phase.

It was originally a World Cup ticket price tracker and was fully renamed
to the bag domain (repo folder renamed from `worldcupticketpricetracker`
to `luxurydesignerbagtracker`). If any ticket/World Cup reference
resurfaces, it's stale — bag domain is correct.

## CRITICAL: do not "fix" the skeletons

- Every `raise NotImplementedError` and `TODO` in `backend/app/*.py` is
  **intentional**. They are the learner's exercises. Do not implement
  them, even if asked to "make the tests pass", unless the owner
  explicitly says to write solutions.
- Failing tests are the expected starting state: tests define the target
  behavior. ~33 tests total; with an unmodified skeleton, ~27 collect and
  fail with `NotImplementedError`.
- `tests/test_db_store.py` fails at **collection** with a SQLAlchemy
  "could not assemble any primary key columns for mapped table
  'price_points'" error until the learner fills in `PricePointORM`'s
  columns. This is expected and documented in `docs/05-database.md`.
- `app/db_models.py` has `price_history = None  # replace with relationship(...)`
  — also an intentional exercise.

## Structure & curriculum

- `LearningPlan.md` — two parts: a general 26-week full-stack roadmap,
  then the project-specific phase plan (Phase 0 through Phase 8).
- `backend/TASKS.md` — granular checkbox list, the learner's main
  worksheet. Includes "concept check" items.
- `backend/docs/00-concepts.md` — from-zero primer (API, CRUD, tables,
  MVC) written for a non-programmer, using this project as the example.
- `backend/docs/01..08-*.md` — one guide per phase (concepts, steps,
  pitfalls, concept-check questions).
- `backend/playground/` — Phase 0 companion: 7 Jupyter notebooks
  (Python warmup, JSON, fake API, CRUD, SQLite SQL, MVC, request flow)
  plus a terminal quiz (`07_quiz.py`), each ending in "✏️ Your turn"
  exercise cells. `playground/scripts/` holds the same 00–06 content
  as plain stdlib-only .py scripts (terminal fallback) — if one is
  edited, mirror the change in the other. All of it is *complete
  working code by design* — the "don't fix skeletons" rule doesn't
  apply here, and conversely don't convert it into NotImplementedError
  skeletons. Safe for the learner to edit/break; reset with
  `git checkout -- backend/playground/`. Notebooks run via ipykernel
  (in requirements.txt) in VS Code.
- Phases: 1 models (dataclasses) → 2-3 BagStore (dicts/heaps, CRUD) →
  4 FastAPI (`/bags` endpoints) → 5 JSON storage → 5.5 Docker Postgres +
  SQLAlchemy (`SqlBagStore`, same interface as `BagStore`) → 6 httpx
  scraper (respx-mocked tests) → 7 alerts (deque) → 8 Claude tool-use
  agent (FakeClient in tests, no API key needed).

## Domain model

`Bag(id, brand, model, color, condition: BagCondition, source,
price_history: list[PricePoint])`. `BagCondition` = new / like_new /
gently_used / vintage. Secondary index is **by brand** (`by_brand`).
DB tables: `bags` + `price_points` (FK `bag_id`), Postgres db name
`bagtracker` (docker-compose).

## Conventions

- Style of skeletons: docstring explains the concept, `TODO:` bullets
  give hints, body is `raise NotImplementedError`. Keep new exercises in
  the same style — hints, not solutions.
- Tests are written for beginners: heavily commented, one phase per file,
  runnable with `pytest -v tests/test_<phase>.py` from `backend/`.
- Guides link back to `docs/00-concepts.md` sections via "Where this
  fits" callouts and end with spoken "concept check" questions — keep
  that pattern when adding phases.
- Sample data: `backend/data/sample_bags.json` (cheapest bag is
  `coach-tabby-001` — `test_load_sample_bags` depends on that).
- Env: `python3 -m venv .venv` in `backend/`, `pip install -r
  requirements.txt`. Postgres via `docker compose up -d` (only needed for
  manual Phase 5.5 checks; its tests use in-memory SQLite).
