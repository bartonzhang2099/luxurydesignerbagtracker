# Phase 0 — Concepts from Zero

Read this **before writing any code**. No programming knowledge needed.
Every idea here will show up again, concretely, in a later phase — this
page is the map; the phases are the territory.

The four big ideas: **API**, **CRUD**, **database tables**, and
**MVC (Model-View-Controller)**.

> **Want to poke the ideas, not just read them?** Every section below
> has a matching interactive notebook in [../playground/](../playground/)
> — run it cell by cell, edit anything, safe to break, nothing graded.
> Best rhythm: read a section here, then play its notebook. The
> playground README has the full map (and the 2-minute setup).

---

## 1. What is a backend? What is an API?

When you browse a resale site like Fashionphile or The RealReal, two
programs are talking to each other:

- the **frontend** — the page in your browser (buttons, photos, filters)
- the **backend** — a program running on a computer somewhere else (a
  "server") that owns the actual data and the rules

The frontend is the waiter; the backend is the kitchen. You (the user)
never walk into the kitchen — you tell the waiter what you want, and the
waiter brings back a dish.

An **API** (Application Programming Interface) is the *menu*: the fixed
list of things you're allowed to ask the kitchen for, and the form the
answer comes back in. In this project, the menu looks like:

| What you ask | How you ask it |
|---|---|
| "show me all the bags" | `GET /bags` |
| "show me bag chanel-flap-001" | `GET /bags/chanel-flap-001` |
| "show me the 5 cheapest bags" | `GET /bags/cheapest?n=5` |
| "here's a new bag listing, please save it" | `POST /bags` + the bag's details |

Each line is called an **endpoint**. Anatomy of one request:

```
GET /bags/cheapest?n=5
─┬─ ─────┬───────── ─┬─
 │       │           └─ query parameter: extra options ("n is 5")
 │       └─ path: WHICH thing you want
 └─ method (verb): WHAT KIND of action
```

The common methods:

- **GET** — read something (asks, changes nothing)
- **POST** — create something new
- **PUT / PATCH** — update something that exists
- **DELETE** — remove something

The answer comes back as **JSON** — a plain-text format both humans and
programs can read:

```json
{ "id": "chanel-flap-001", "brand": "Chanel", "current_price": { "price": 9500.0, "currency": "USD" } }
```

Curly braces = an object ("a thing with named fields"). Square brackets =
a list. That's 90% of JSON.

The answer also has a **status code**: `200` = OK, `201` = created,
`404` = not found, `500` = the kitchen caught fire (server bug).

> **In this project:** you *build* the kitchen. Phase 4 is where you
> write the menu (`app/main.py`), and you'll see all of this again there.

---

## 2. What is CRUD?

Almost every app you've ever used — Instagram, Notes, a shopping app —
is, underneath, the same four operations on some data:

| Letter | Operation | Plain English | In this project (Phase 2) | As an API endpoint (Phase 4) |
|---|---|---|---|---|
| **C** | Create | "add a new one" | `store.add(bag)` | `POST /bags` |
| **R** | Read | "show me" | `store.get(id)`, `store.all()` | `GET /bags`, `GET /bags/{id}` |
| **U** | Update | "change it" | `bag.add_price(...)` | (stretch goal: `PATCH /bags/{id}`) |
| **D** | Delete | "remove it" | `store.remove(id)` | (stretch goal: `DELETE /bags/{id}`) |

A post on Instagram? Create. Your feed? Read. Editing a caption? Update.
Deleting a post? Delete. Once you see CRUD, you can't unsee it — and
"can you build a CRUD app" is the baseline question behind most junior
backend interviews.

> **In this project:** Phase 2 is CRUD *in memory* (Python dictionaries),
> Phase 4 exposes it *over an API*, Phase 5.5 moves it into a *real
> database*. Same four verbs, three different layers — that repetition is
> intentional.

---

## 3. What is a database table?

A **table** is a spreadsheet with rules.

Like a spreadsheet, it has **columns** (the fields, each with a fixed
type) and **rows** (one per thing). Here's this project's `bags` table:

| id (text, **primary key**) | brand (text) | model (text) | color (text) | condition (enum) |
|---|---|---|---|---|
| chanel-flap-001 | Chanel | Classic Flap Medium | Black Caviar | like_new |
| lv-neverfull-001 | Louis Vuitton | Neverfull MM | Damier Ebene | gently_used |

Unlike a spreadsheet:

- **Types are enforced.** You can't put "hello" in a number column —
  the database refuses. Bad data gets stopped at the door.
- Every table has a **primary key** — a column guaranteed unique per row
  (here, `id`). It's how you point at *exactly one* row.
- Tables can **reference each other** with a **foreign key**. Our second
  table, `price_points`, stores every price observation, and its
  `bag_id` column points back at `bags.id`:

```
bags                                price_points
┌──────────────────┬────────┐       ┌────┬──────────────────┬────────┬─────────────┐
│ id (PK)          │ brand  │       │ id │ bag_id (FK)      │ price  │ timestamp   │
├──────────────────┼────────┤       ├────┼──────────────────┼────────┼─────────────┤
│ chanel-flap-001  │ Chanel │ ◄──── │ 1  │ chanel-flap-001  │ 9500.0 │ 2026-01-01  │
│                  │        │ ◄──── │ 2  │ chanel-flap-001  │ 9800.0 │ 2026-02-01  │
└──────────────────┴────────┘       └────┴──────────────────┴────────┴─────────────┘
```

One bag, many price points — a **one-to-many relationship**. This is why
it's called a *relational* database. Why two tables instead of cramming
prices into the bag row? Because a bag can have 2 price observations or
200 — rows are made for "we don't know how many".

You talk to a database in **SQL**, a small English-like language:

```sql
SELECT * FROM bags WHERE brand = 'Chanel';
```

("give me every column of every row in `bags` where the brand column
says Chanel.")

> **In this project:** Phase 5.5. You'll define both tables as Python
> classes (an "ORM" writes the SQL for you), run a real PostgreSQL
> database with Docker, and poke at it with raw SQL yourself.

---

## 4. What is MVC (Model-View-Controller)?

As soon as a program grows past one file, you need a rule for *what goes
where*. MVC is the most famous such rule. It splits an app into three
jobs:

- **Model** — *what the data is and what it can do.* "A Bag has a brand,
  a model, a condition, a price history; you can ask it for its current
  price." Knows nothing about the web.
- **View** — *what the outside world sees.* In a classic website, the
  HTML page. In an API backend like ours, the **JSON shape** of a
  response — which fields go out, named what.
- **Controller** — *the traffic cop in between.* Receives a request,
  decides which model functions to call, hands the result to the view.
  Contains no business logic itself — it just coordinates.

In this repo:

```
            request: GET /bags/cheapest?n=5
                          │
                          ▼
   CONTROLLER   app/main.py ─ route functions: parse the request,
                              call the model, return the response
                          │
                          ▼
   MODEL        app/models.py    ─ Bag, PricePoint ("what a bag is")
                app/store.py     ─ BagStore ("how bags are kept/found")
                app/db_models.py ─ same idea, backed by a real database
                          │
                          ▼
   VIEW         app/schemas.py ─ BagResponse: the JSON shape sent back
```

The payoff is swappability: in Phase 5.5 you replace the in-memory
`BagStore` with a database-backed `SqlBagStore`, and **`main.py` barely
changes** — because the controller never cared *how* the model stored
things. That moment is MVC earning its keep, live.

Two honest footnotes: FastAPI projects usually say "router" instead of
"controller" and "schema" instead of "view" — same roles, different
names. And `store.py` is technically a sub-layer of the model called a
*repository* — worth knowing the word, not worth worrying about yet.

---

## 5. How a request actually flows (tying it together)

What happens when someone calls `GET /bags/cheapest?n=2` on the finished
project:

1. The request arrives at the server (FastAPI, in `main.py`).
2. FastAPI matches the path to the `cheapest_bags` **controller**
   function, and parses `n=2` into a Python `int`.
3. The controller calls the **model**: `store.cheapest(2)`.
4. The store walks its bags (in Phase 5.5: queries the **table**) and
   returns the two cheapest `Bag` objects — that's the **R** in CRUD.
5. The controller converts each `Bag` into a `BagResponse` — the
   **view**.
6. FastAPI turns those into **JSON**, attaches status code `200`, and
   sends it back.

Six steps, four concepts, one request. Every phase in this project builds
one piece of this pipeline.

---

## Check yourself (no code — just say the answers out loud)

1. In the restaurant analogy, what are the waiter, the kitchen, and the
   menu?
2. You favorite a bag on a resale app. Which CRUD letter is that? You
   scroll the listings — which letter?
3. Why does `price_points` get its own table instead of storing prices
   inside the `bags` table?
4. What's the difference between a primary key and a foreign key?
5. A bug makes `GET /bags` show the right prices but label them all
   "EUR" instead of "USD" (the numbers are right, the label is wrong).
   Is that probably a model, view, or controller bug?
6. Why can `main.py` stay almost unchanged when the storage moves from a
   Python dict to PostgreSQL?

If you can answer these in your own words, you're ready —
go to [Phase 1](01-models.md).

<details>
<summary>Answers (click after you've tried)</summary>

1. Waiter = frontend, kitchen = backend, menu = API.
2. Favoriting = Create (a new "favorite" record is created) or Update —
   either answer shows understanding. Scrolling = Read.
3. A bag has an unknown, growing number of price observations — "many of
   a thing" becomes rows in a separate table pointing back at the owner.
4. Primary key: uniquely identifies a row *in its own table*. Foreign
   key: a column that *points at* another table's primary key.
5. View — the data is right, the outgoing shape/label is wrong
   (`schemas.py` / the response-building code).
6. Because the controller only calls model methods like `cheapest(n)`
   and never cares how they're implemented — both stores offer the same
   methods.

</details>
