# Playground 🛝

Tiny, **safe-to-break** interactive notebooks for *feeling* the Phase 0
concepts before you build anything. Nothing in here is graded, nothing
has tests, and you cannot break the real project from this folder —
edit recklessly.

## One-time setup (~2 minutes)

The playground is made of **Jupyter notebooks** (`.ipynb` files) — code
split into cells you run one at a time, with the output appearing right
below each cell. Edit a cell, re-run it, watch the output change.

**Easiest way — VS Code (recommended):**

1. Do the venv steps from [TASKS.md](../TASKS.md) "Setup" (`python3 -m
   venv .venv`, activate, `pip install -r requirements.txt` — that now
   includes the notebook kernel).
2. Open any `.ipynb` file in VS Code. If it asks for a *kernel*, pick
   the `.venv` Python. (VS Code may offer to install its Jupyter
   extension — say yes.)
3. Click ▶ next to a cell, or press **Shift+Enter**, to run it.

**Alternative — in the browser:**

```bash
pip install jupyterlab
jupyter lab        # run from backend/ — opens in your browser
```

## How to use it

1. Read the matching section of [docs/00-concepts.md](../docs/00-concepts.md) first.
2. Open the notebook and run it cell by cell, top to bottom, reading as
   you go.
3. Every notebook ends with **✏️ Your turn** cells: small edits to make,
   then re-run and watch the output change. *That* loop — predict, edit,
   run, compare — is where the learning happens. Reading alone doesn't
   stick.

## The notebooks

| Notebook | Concept | Primer section |
|---|---|---|
| `00_python_warmup.ipynb` | variables, lists, dicts, loops, functions | (none — pre-basics) |
| `01_json.ipynb` | what JSON is | §1 |
| `02_api_kitchen.ipynb` | backend, API, endpoints, status codes | §1 |
| `03_crud.ipynb` | Create / Read / Update / Delete | §2 |
| `04_tables_sql.ipynb` | tables, primary/foreign keys, **real SQL** | §3 |
| `05_mvc.ipynb` | Model–View–Controller, swappability | §4 |
| `06_request_flow.ipynb` | one request through all the layers, one cell per step | §5 |
| `07_quiz.py` | interactive "check yourself" quiz (terminal) | §6 |

Go in order — each one leans on the previous. The quiz is a plain
terminal script: `python3 playground/07_quiz.py` from `backend/`.

The [scripts/](scripts/) folder has the same 00–06 content as plain
Python scripts (`python3 playground/scripts/01_json.py`) — a fallback
if notebooks aren't working for you; no setup needed beyond Python.

## Rules of the playground

- **You cannot break anything.** Worst case, a cell shows a red error.
  Read it (last line first!), fix, re-run. Reading errors calmly is
  half of programming.
- Cells share memory top-to-bottom. If a notebook gets into a weird
  state (e.g. "table already exists"), use **Run All** to start fresh.
- If you want a pristine copy back: `git checkout -- backend/playground/`
- Done with all eight? Head back to [TASKS.md](../TASKS.md) Phase 1.
