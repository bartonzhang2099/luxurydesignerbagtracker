# Luxury Bag Price Tracker

A learning project: build a backend service that tracks luxury designer
bag prices (Chanel, Hermès, Louis Vuitton, ...) over time, from the
ground up.

This repo is structured as a guided curriculum — see
[LearningPlan.md](LearningPlan.md) for the full phase-by-phase plan
(data structures → REST API → persistence → database → real data
fetching → alerts → AI agent integration). Each phase also has a written
guide in [backend/docs/](backend/docs/).

**New here?** Read
[backend/docs/00-concepts.md](backend/docs/00-concepts.md) first — a
from-zero primer on APIs, CRUD, database tables, and MVC, using this
project as the running example. Then work through
[backend/TASKS.md](backend/TASKS.md) — a checkbox-by-checkbox list of
every small step, in order.

## Folder structure

```
backend/
  app/
    models.py     # Phase 1: Bag / PricePoint data structures
    store.py       # Phase 2-3: BagStore (indexing, sorting, searching)
    schemas.py      # Phase 4: API request/response shapes (Pydantic)
    main.py          # Phase 4: FastAPI app & routes
    storage.py        # Phase 5: JSON persistence
    db.py               # Phase 5.5: SQLAlchemy engine/session setup
    db_models.py         # Phase 5.5: ORM models (BagORM, PricePointORM)
    db_store.py            # Phase 5.5: SqlBagStore (Postgres-backed)
    scraper.py                # Phase 6: fetching real bag price data
    alerts.py                   # Phase 7: price alert rules
    agent.py                       # Phase 8: AI agent (Claude tool use)
  data/
    sample_bags.json                 # seed data used by Phase 5+
  docs/
    00-concepts.md                     # from-zero primer (API/CRUD/tables/MVC)
    01-models.md ... 08-agent.md        # one guide per phase
  tests/
    test_*.py                             # one test file per phase
  docker-compose.yml                        # Phase 5.5: local Postgres
  .env.example                                # Phase 5.5: DATABASE_URL
  requirements.txt
```

Each `app/*.py` file is a skeleton with `TODO`s and
`raise NotImplementedError` markers. Implement them one phase at a time,
guided by `docs/` and checked against `tests/`.

## Quick start

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Once Phase 4 is implemented, run the API:

```bash
uvicorn app.main:app --reload
```
