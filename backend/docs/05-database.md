# Phase 5.5 Guide — Local Database with Docker + SQLAlchemy

**Files to edit:** `app/db.py`, `app/db_models.py`, `app/db_store.py`
**Tests:** `pytest -v tests/test_db_store.py`

> **Where this fits:** this is where
> [tables](00-concepts.md#3-what-is-a-database-table) become real. The
> `bags` and `price_points` tables sketched in the concepts primer are
> exactly what you'll create here, including the one-to-many foreign-key
> relationship. And because `SqlBagStore` keeps the same CRUD methods as
> `BagStore`, you'll also see the MVC payoff: swap the model's storage,
> the controller (`main.py`) doesn't care.

## Why this phase matters

JSON files (Phase 5) work, but every real backend job you'll interview for
uses a database. This phase introduces:
- **Docker**: running a Postgres server locally without installing it
  directly on your machine.
- **SQLAlchemy ORM**: mapping Python classes to SQL tables, and writing
  queries as Python instead of raw SQL strings.

By the end, `SqlBagStore` will support the exact same operations as the
in-memory `BagStore` from Phase 2-3 - just backed by a real database.

## Concepts

### Docker & docker-compose

- A **container** is a lightweight, isolated environment running a single
  program (here, Postgres) - no need to install Postgres on your machine.
- `docker-compose.yml` describes one or more containers ("services") and
  how to run them. Read:
  [Docker Compose overview](https://docs.docker.com/compose/).
- `docker compose up -d` starts the `db` service in the background.
  `docker compose down` stops it. `docker compose down -v` also deletes
  the data volume (fresh start).

### SQLAlchemy

- **`create_engine(url)`**: represents a connection pool to a database.
  The URL encodes the driver, credentials, host, port, and database name -
  see `.env.example`.
- **Declarative models**: a Python class inheriting from `Base`, with
  `Column(...)` class attributes, maps to a SQL table. Read:
  [SQLAlchemy ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).
- **`relationship()`**: links two ORM models (here, a `BagORM` has many
  `PricePointORM`s) so you can access `bag.price_history` as a Python
  list, with SQLAlchemy handling the JOIN/foreign key underneath.
- **`Session`**: represents a single "conversation" with the database -
  you add/query/delete objects, then `commit()` to persist changes.

> **Note:** until you fill in `PricePointORM`'s columns, running
> `pytest tests/test_db_store.py` will fail at *collection* time with
> `Mapper ... could not assemble any primary key columns for mapped table
> 'price_points'`. That's expected - it's SQLAlchemy telling you exactly
> what's missing. Other test files are unaffected.

## Step-by-step

### 1. Start Postgres

```bash
cd backend
docker compose up -d
docker compose ps   # should show "db" as healthy
cp .env.example .env
```

`app/db.py` reads `DATABASE_URL` from the environment (defaulting to the
`docker-compose.yml` credentials), so once the container is running and
the variable is exported (or you rely on the default), you're ready to
connect.

### 2. Define the ORM models (`app/db_models.py`)

`BagORM` is mostly written for you - read it first. Then:
- Fill in `PricePointORM`'s columns (`id`, `bag_id`, `price`,
  `currency`, `timestamp`) and its `bag` relationship.
- Fill in `BagORM.price_history` as the other side of that relationship.

### 3. Wire up `init_db` (`app/db.py`)

Import `app.db_models` (so the classes register themselves on
`Base.metadata`) and call `Base.metadata.create_all(bind=engine)`.

### 4. Implement `SqlBagStore` (`app/db_store.py`)

Work through each method - they mirror `BagStore` from Phase 2-3:
- `_to_dataclass`: ORM object -> `Bag` dataclass (the reverse of what
  you did for JSON in Phase 5, but from ORM objects instead of dicts).
- `add`, `get`, `remove`, `all`, `by_brand`: straightforward
  session/query operations - see the docstrings for the exact SQLAlchemy
  calls.
- `cheapest`, `filter_by_price_range`: for now, fetch everything with
  `self.all()` and reuse your Phase 3 `heapq`/filtering logic in Python.

## Common pitfalls

- **Forgetting `init_db()`**: tables won't exist and queries will fail
  with "relation does not exist" (Postgres) or "no such table" (SQLite).
- **Session lifetime**: don't return ORM objects directly from a method
  after the session closes - access to their relationships (like
  `price_history`) may fail with a "DetachedInstanceError". Convert to
  your `Bag` dataclass *before* the session closes (i.e. inside the
  `with self._session_factory() as session:` block).
- **Enum mismatch**: `SAEnum(BagCondition)` stores the *enum member
  name* (e.g. `"LIKE_NEW"`) by default in some configurations - if you
  hit a mismatch with the JSON storage's `.value` (`"like_new"`), that's
  why. For this phase it's fine as long as it round-trips consistently.

## Inspecting the database directly

```bash
docker compose exec db psql -U postgres -d bagtracker
# inside psql:
\dt                  -- list tables
SELECT * FROM bags;
SELECT * FROM price_points;
\q
```

## Check your work

```bash
pytest -v tests/test_db_store.py
```

These tests run against an in-memory SQLite database, so they pass without
Docker - but try the manual `psql` steps above against the real Postgres
container too. Once green, continue to [Phase 6](06-scraper.md).

## Concept check (say it out loud)

1. In the `price_points` table, which column is the primary key and
   which is the foreign key? What does each one guarantee?
2. Why is `price_points` a separate table instead of extra columns on
   `bags` (like `price1`, `price2`, `price3`...)?
3. You swapped `BagStore` for `SqlBagStore` and `main.py` didn't change.
   Which MVC principle is that demonstrating?
4. Write (or just say) the SQL to fetch every price point for bag
   `chanel-flap-001`, then check yourself in `psql`.

## Stretch goals

- Swap `store = BagStore()` in `app/main.py` for
  `store = SqlBagStore()` - since both implement the same interface,
  the API routes shouldn't need to change.
- Push `cheapest`/`filter_by_price_range` into real SQL queries
  (`ORDER BY`, `LIMIT`, `WHERE`) instead of filtering in Python.
- Look into [Alembic](https://alembic.sqlalchemy.org/) for managing schema
  changes ("migrations") over time.
