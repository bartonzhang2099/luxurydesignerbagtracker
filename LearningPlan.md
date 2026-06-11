# Full-Stack Dev Learning Plan (0 → Job-Ready)

## 1. Overview & Philosophy

This 26-week plan takes a beginner (or rusty developer) from zero to job-ready full-stack engineer. It emphasizes:

- **Consistency over intensity** — small daily/weekly progress beats cramming.
- **Real projects + strong fundamentals** (Python → Backend → Full-stack → AI features).
- **DSA running in parallel** the entire time (non-negotiable for interviews).
- **Mentorship via Pull Requests** (highest leverage feedback loop).
- **Public portfolio** that speaks for itself in interviews.

The mentee works ~20 hours/week. If life intervenes and it becomes ~10 hrs/week, the plan simply stretches to ~12 months — the **order never changes**.

---

## 2. The GitHub Repo (set this up on your personal machine first)

Create a single repo that will hold the entire journey:

```bash
# On your machine (mentor)
gh repo create fullstack-journey --public --clone
cd fullstack-journey

# Recommended initial structure (create these folders)
mkdir -p 01-python-foundations/exercises
mkdir -p 02-backend-core
mkdir -p 03-production-backend
mkdir -p 04-capstone
mkdir -p 05-ai-agents-rag

# Initial files
echo '# Full-Stack Journey' > README.md
echo 'python' > .gitignore
git add .
git commit -m "chore: initial repo structure"
git push -u origin main
```

### Recommended CI (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pytest
```

Now every push runs tests + linter automatically. A green check = the exercise is correct.

---

## 3. The Mentoring Workflow (how you give Feedback)

This is the highest-leverage part. Mentor asynchronously through Pull Requests.

```sh
# mentor loop, every assignment:
git switch -c week-01-python   # branch per assignment
# ... do the work, make tests pass ...
git add .
git commit -m "Week 1: variables & loops exercises"
git push -u origin week-01-python
gh pr create --fill   # opens a Pull Request
```

### Your Loop:

1. CI runs her tests automatically — you instantly see pass/fail.
2. Open the PR's **Files changed** tab and leave **inline comments** on the code ("this works, but here's the idiomatic way", "what happens if the list is empty?").
3. You either **request changes** (she iterates on the same branch) or **approve & merge**.
4. The merged work lands on `main`; she starts the next branch.

### Pro Tips

- Use **GitHub Issues** as the assignment list. Create one Issue per week/topic ("Week 2: FastAPI CRUD endpoints"), with a checklist of tasks. Optionally create a GitHub Projects board (Backlog → In Progress → In Review → Done) for visibility.
- **Weekly cadence**: one ~30-45 min live call (you two) to review the week, unblock, and set next week's Issues. Async PR comments handle the rest.
- **Beginner git rules** (set these early):
  - Small commits with clear messages
  - Never commit secrets (`.env` is gitignored)
  - One branch per assignment
  - Always `git pull --rebase origin main` before starting new work

---

## 4. The Curriculum (~26 weeks @ 20 hrs/week)

### Weekly rhythm (the default 20 hours)

| Track              | Focus                                      | Time   |
|--------------------|--------------------------------------------|--------|
| **Build track**    | Current phase's main work (Python → backend → capstone + AI) | ~10h  |
| **DSA**            | 3-5 problems, one pattern at a time        | ~5-6h |
| **Learning**       | Watching/reading for the current topic     | ~3h   |
| **Review + Log**   | Respond to PR comments, weekly log         | ~1-2h |

> **DSA is non-negotiable** and runs the full 26 weeks. Consistency (a little every week) beats cramming.

---

### Phase 0 — Setup & Terminal (Week 0, ~3-5 days)

**Goal**: A working dev environment and "I can run code."

- Install Python 3.12+, VS Code (or PyCharm) + Ruff extension, `git`, GitHub account, SSH keys.
- Learn terminal basics (`cd`, `ls`, `mkdir`, `cat`, pipes, etc.).
- What `git` is, how to clone, commit, push, and open a PR.
- **Milestone**: Clone the repo, run the "hello world" example, make her first commit + PR.

**Resources**:
- [The Missing Semester (MIT)](https://missing.csail.mit.edu/)
- [uv docs](https://docs.astral.sh/uv/)

---

### Phase 1 — Python Foundations + DSA begins (Weeks 1-4)

**Goal**: Confident, idiomatic Python + first DSA patterns.

**Topics**:
- Python core: variables, types, control flow, `collections`/`dataclasses`, functions, comprehensions, OOP basics (classes, inheritance), modules, error handling, `argparse`, reading tracebacks, `pytest` basics.
- DSA: `collections`, `bisect`, basic patterns — **3 problems/week**.

**Milestone**: Build 3 small CLI tools:
1. To-do manager
2. Number-guessing game
3. CSV expense summarizer

**Resources**:
- [Python Crash Course (3rd ed.)](https://nostarch.com/python-crash-course-3rd-edition) — best beginner book
- [freeCodeCamp Python Full Course (YouTube)](https://www.youtube.com/watch?v=rfscVS0vtbw)
- [Exercism Python track](https://exercism.org/tracks/python) (free + mentoring)
- DSA: [NeetCode Roadmap](https://neetcode.io/roadmap) — follow the order

---

### Phase 2 — Backend Core (HEAVY) + SQL + DSA (Weeks 5-9)

**Goal**: Build real REST APIs backed by a real database. This is the centerpiece of the plan.

**Topics**:
- **FastAPI** fundamentals: routing, path/query params, Pydantic v2 models & validation, `async`/`await`, dependency injection, testing, middleware.
- **Databases**: SQL fundamentals (SELECT/INSERT/UPDATE/DELETE/JOINs/indexes/transactions), data modeling & normalization, PostgreSQL, SQLAlchemy 2.0 + Alembic migrations.
- Auth: password hashing, JWT.
- **Milestone**: Full CRUD API with auth, tests, and deployment (Railway/Render/Fly).

**Resources**:
- [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [TestDriven.io FastAPI Course](https://testdriven.io/courses/fastapi/) (paid, excellent) or [freeCodeCamp FastAPI (YouTube)](https://www.youtube.com/watch?v=0sOvCWC0B5k)
- SQL: [SQLBolt](https://sqlbolt.com/) + [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- Free Postgres: [Neon](https://neon.tech/) or [Supabase](https://supabase.com/)
- DSA: NeetCode 150 (continue steadily)

---

### Phase 3 — Production Backend + Minimal Frontend + DSA (Weeks 10-13)

**Goal**: Professional project structure + first full-stack experience.

**Topics**:
- Backend: layered architecture, environment config, background tasks (Celery/ARQ), logging, pagination, error handling, webhooks, deployment best practices.
- Frontend (just enough): HTML/CSS + Tailwind, JavaScript/TypeScript basics, shadcn/ui components, Next.js App Router basics, edge functions.
- Advanced: CSS animations, SSR concepts, build tooling.
- DSA: Arrays → Trees → Heaps / Priority Queues (increase to ~4-5 problems/week).

**Milestone**: Deploy the Task API publicly + a small React/Next.js frontend that talks to it. First real full-stack deploy + public URL.

**Resources**:
- [Next.js Docs](https://nextjs.org/docs) + [Learn Next.js](https://nextjs.org/learn)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [Docker Getting Started](https://docs.docker.com/get-started/)

---

### Phase 4 — Capstone + Interview DSA Ramp (Weeks 14-18)

**Goal**: One portfolio-grade full-stack application + interview readiness.

**Topics**:
- **Capstone**: Pick something real and useful (habit tracker, small marketplace, expense splitter, AI-powered tool, etc.). Must include:
  - FastAPI backend + Postgres + auth + tests
  - Next.js frontend
  - Deployed (Railway/Render/Fly + Vercel)
  - Excellent README + 2-minute demo video
- DSA ramp: Backtracking → Graphs → 1-2 Dynamic Programming problems. Start **timed** practice. Increase volume to ~5 problems/week.
- Soft skills: Resume bullet writing, LinkedIn/GitHub polish, behavioral stories.

**Resources**:
- [NeetCode 150](https://neetcode.io/practice)
- [Tech Interview Handbook](https://www.techinterviewhandbook.org/)

---

### Phase 5 — AI Agents + RAG (Weeks 19-26)

**Goal**: The differentiator — add modern AI capabilities on top of solid backend skills.

**Topics**:
- LLM API basics (Claude / OpenAI), prompt engineering, structured outputs (Pydantic).
- `embeddings` + vector search with `pgvector` (reuses existing Postgres!).
- Chunking strategies, retrieval pipelines → full RAG.
- Agentic workflows: tool/function calling → agent frameworks (LangGraph preferred for production fit with FastAPI).
- Evaluation: how to measure RAG/agent quality (faithfulness, relevance, hallucination metrics).

**Milestone Project**:
A production-grade tool-using agent:
- Upload documents → ask questions → get cited answers
- FastAPI backend + pgvector + simple Next.js UI
- Or: an assistant that can query her own APIs / database / the web via tools

**Resources**:
- [Anthropic Cookbook](https://docs.anthropic.com/) & [OpenAI Platform Docs](https://platform.openai.com/docs)
- [LangGraph Docs](https://python.langchain.com/docs/langgraph) (use selectively)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [pgvector](https://github.com/pgvector/pgvector)

> **Reality check**: The agent framework landscape changes fast. Teach **fundamentals** deeply (embeddings, retrieval, tool calling, evaluation). Treat any specific framework as swappable. Building a from-scratch RAG pipeline (no framework) is often the best learning exercise.

---

## 5. After the Plan: Getting the Job

By the end the mentee should have:

- **3-4 polished public repos** (capstone and RAG app are the headliners; others show progression).
- **~150+ DSA problems** solved (NeetCode 150 completed + extras).
- Strong **resume** with impact-focused project bullets.
- Active **LinkedIn + GitHub** (weekly commits visible).
- Mock interviews + live-coding practice completed.
- A compelling story: "I went from X to building production full-stack apps with AI features in 6-12 months."

---

## 6. First 3 Things to Do (Right Now)

1. **Create the repo** using the commands in Section 2.
2. **Add the CI workflow** + write 2-3 starter `pytest` exercises in `01-python-foundations/exercises/` so she has something concrete to pass in Week 1.
3. **Open the first GitHub Issue**: `Phase 0: Set up your environment + first PR`.

---

**Good luck!** This plan is battle-tested in structure and focuses on the highest-ROI activities for breaking into software engineering roles. Consistency + real projects + strong mentorship feedback = results.

---

# Project-Specific Plan: Luxury Bag Price Tracker

This section is the concrete, hands-on project that anchors **Phase 2-3
(Backend Core / Production Backend)** above. Skeleton code for every phase
lives in `backend/app/`, with `TODO`s and `raise NotImplementedError`
markers for the participant to fill in. Tests in `backend/tests/` verify
each phase.

Each phase has:
- **Concepts** to learn before/while doing the phase
- **Files to edit**
- **Goal / "done when"** criteria

Work through phases in order — each builds on the last. For a granular,
checkbox-level breakdown, see [backend/TASKS.md](backend/TASKS.md).

## Phase 0 — Concepts from Zero (read before any code)

**Guide:** [backend/docs/00-concepts.md](backend/docs/00-concepts.md)

A no-code primer (~15 min) explaining what an **API**, **CRUD**, a
**database table**, and **MVC** are — using this project as the running
example, with self-check questions at the end. Every later phase links
back to it when its concept appears for real.

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Run the API (once Phase 4 is done):

```bash
uvicorn app.main:app --reload
```

## Phase 1 — Modeling a Bag (dataclasses, enums, basic OOP)

**Guide:** [backend/docs/01-models.md](backend/docs/01-models.md)

**Concepts:** `dataclass`, `Enum`, type hints, `Optional`, methods on data
objects.

**Files:** `backend/app/models.py`, `backend/tests/test_models.py`

**Goal:** Implement `PricePoint`, `Bag`, and:
- `Bag.add_price(...)` — append a price observation to history
- `Bag.current_price()` — most recent price, or `None`
- `Bag.price_change()` — difference between latest two prices

**Done when:** `pytest -v tests/test_models.py` passes.

## Phase 2 — BagStore (hash maps, lists, indexing)

**Guide:** [backend/docs/02-store.md](backend/docs/02-store.md)

**Concepts:** dictionaries for O(1) lookup, secondary indexes, lists,
iteration.

**Files:** `backend/app/store.py`, `backend/tests/test_store.py`

**Goal:** Implement an in-memory `BagStore`:
- `add(bag)` — store by id, and index by brand
- `get(bag_id)` — O(1) lookup
- `remove(bag_id)` — remove from both indexes
- `all()` — iterate all bags
- `by_brand(brand)` — all bags for a given brand (secondary index)

**Done when:** `test_basic_crud` and `test_by_brand_index` pass.

## Phase 3 — Sorting & Searching (heaps, comparisons)

**Guide:** [backend/docs/02-store.md](backend/docs/02-store.md) (same file
as Phase 2 — `BagStore` is built incrementally)

**Concepts:** `heapq`, sorting with `key=`, filtering, time complexity.

**Files:** `backend/app/store.py` (continue), `backend/tests/test_store.py`

**Goal:** Implement:
- `cheapest(n)` — `n` bags with lowest current price, via
  `heapq.nsmallest`
- `filter_by_price_range(min_price, max_price)` — bags whose current
  price falls in range

**Done when:** `test_cheapest` and `test_filter_by_price_range` pass.

## Phase 4 — Backend API (FastAPI, REST, Pydantic)

**Guide:** [backend/docs/03-api.md](backend/docs/03-api.md)

**Concepts:** REST endpoints, path/query params, request/response models
with Pydantic.

**Files:** `backend/app/main.py`, `backend/app/schemas.py`,
`backend/tests/test_api.py`

**Goal:** Implement endpoints backed by a shared `BagStore`:
- `GET /bags` — list all bags
- `GET /bags/{bag_id}` — single bag (404 if missing)
- `GET /bags/cheapest?n=5` — cheapest n bags
- `POST /bags` — add a new bag listing from a validated JSON body

**Done when:** `pytest -v tests/test_api.py` passes (FastAPI `TestClient`).

## Phase 5 — Persistence (JSON file storage)

**Guide:** [backend/docs/04-storage.md](backend/docs/04-storage.md)

**Concepts:** serialization, file I/O, round-tripping objects to/from JSON.

**Files:** `backend/app/storage.py`, `backend/tests/test_storage.py`

**Goal:** Implement:
- `save_store(store, path)` — write bags + price history to JSON
- `load_store(path)` — reconstruct a `BagStore` from that JSON

Wire `main.py` to load `data/sample_bags.json` on startup if present.

**Done when:** `pytest -v tests/test_storage.py` passes (save → load
round-trip).

## Phase 5.5 — Local Database with Docker + SQLAlchemy

**Guide:** [backend/docs/05-database.md](backend/docs/05-database.md)

**Concepts:** Docker/docker-compose, running Postgres locally, SQLAlchemy
ORM models, sessions/queries, relationships.

**Files:** `backend/docker-compose.yml`, `backend/.env.example`,
`backend/app/db.py`, `backend/app/db_models.py`, `backend/app/db_store.py`,
`backend/tests/test_db_store.py`

**Goal:** Run Postgres via `docker compose up -d`, then implement:
- `db_models.py` — `BagORM` / `PricePointORM` SQLAlchemy models with a
  one-to-many relationship
- `db.py` — `init_db()` to create tables
- `db_store.py` — `SqlBagStore`, a SQL-backed implementation of the same
  interface as `BagStore` (`add`, `get`, `remove`, `all`, `by_brand`,
  `cheapest`, `filter_by_price_range`)

**Done when:** `pytest -v tests/test_db_store.py` passes (runs against
in-memory SQLite, no Docker required for tests) — and you've manually
verified data lands in Postgres via `docker compose exec db psql ...`.

## Phase 6 — Real Data: Fetching Bag Prices

**Guide:** [backend/docs/06-scraper.md](backend/docs/06-scraper.md)

**Concepts:** HTTP clients (`httpx`), parsing JSON responses, error
handling, mapping external data into your own models, mocking HTTP in tests.

**Files:** `backend/app/scraper.py`, `backend/tests/test_scraper.py`

**Goal:** Implement:
- `fetch_raw_listings()` — call a bag-price source (configurable via
  `SOURCE_URL` env var) and return raw JSON
- `parse_listing(raw)` — map a raw record into `(bag_id, price, currency)`
- `fetch_and_update(store)` — fetch, parse, and call `bag.add_price(...)`
  for matching bags

> Tests use a **mocked** HTTP response, so no live API key is required to
> develop. Point `SOURCE_URL` at a real source (e.g. a resale marketplace
> feed) to try it for real.

**Done when:** `pytest -v tests/test_scraper.py` passes.

## Phase 7 — Price History & Alerts (queues, time series)

**Guide:** [backend/docs/07-alerts.md](backend/docs/07-alerts.md)

**Concepts:** chronological data, threshold/alerting logic, queues.

**Files:** `backend/app/alerts.py`, `backend/tests/test_alerts.py`

**Goal:** Implement:
- `AlertRule` — a (bag_id, threshold_price) pair — "tell me when the
  Classic Flap drops below $8,000"
- `check_alerts(store, rules)` — returns triggered alerts (current price <=
  threshold)

**Done when:** `pytest -v tests/test_alerts.py` passes.

## Phase 8 — AI Agent: Natural-Language Bag Queries

**Guide:** [backend/docs/08-agent.md](backend/docs/08-agent.md)

**Concepts:** tool/function calling with the Claude API, turning existing
functions (`cheapest`, `by_brand`, `filter_by_price_range`) into "tools" an
LLM can call.

**Files:** `backend/app/agent.py`, new `POST /agent/query` endpoint in
`backend/app/main.py`, `backend/tests/test_agent.py`

**Goal:** Implement:
- `build_tools()` — tool schemas for `cheapest_bags`, `bags_by_brand`,
  `filter_by_price_range`
- `run_agent(query, store)` — sends the question to Claude with those tools,
  executes any tool calls against the `BagStore`, returns a final answer

Example queries: "What are the 3 cheapest bags right now?", "Show me all
the Chanel bags", "Anything between $1,000 and $5,000?"

**Done when:** `pytest -v tests/test_agent.py` (mocked) passes, and
`run_agent(...)` returns a sensible answer.

## Stretch Goals

- Swap JSON file storage for the Phase 5.5 `SqlBagStore` in `main.py`
- Add `/bags/{id}/history` endpoint returning full price history
- Scheduled background job (`apscheduler`) to refresh prices periodically
- Tiny frontend that calls the API (bag cards with price-drop badges!)
- Agent tool to subscribe to alerts via natural language ("tell me if any
  Chanel flap goes under $8k")
