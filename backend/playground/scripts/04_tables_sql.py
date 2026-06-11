"""
PLAYGROUND 04 — Database tables and REAL SQL (no Docker needed)

Run me:   python3 playground/scripts/04_tables_sql.py
Primer:   docs/00-concepts.md, section 3

Surprise: Python ships with a tiny real database called SQLite. The SQL
you type here is the same language you'll use on PostgreSQL in Phase
5.5 — this is the genuine article, just running in memory instead of in
a Docker container. We'll build the primer's exact two tables.
"""

import sqlite3

db = sqlite3.connect(":memory:")           # a database that lives in RAM
db.execute("PRAGMA foreign_keys = ON")     # make it enforce foreign keys

print("=" * 60)
print("1. CREATE the two tables (the 'spreadsheet with rules')")
print("=" * 60)

db.execute("""
    CREATE TABLE bags (
        id        TEXT PRIMARY KEY,   -- unique per row, no exceptions
        brand     TEXT NOT NULL,
        model     TEXT NOT NULL,
        condition TEXT NOT NULL
    )
""")

db.execute("""
    CREATE TABLE price_points (
        id        INTEGER PRIMARY KEY,          -- auto-numbered 1, 2, 3...
        bag_id    TEXT NOT NULL REFERENCES bags(id),   -- the FOREIGN KEY
        price     REAL NOT NULL,
        timestamp TEXT NOT NULL
    )
""")
print("  tables 'bags' and 'price_points' created.\n")

print("=" * 60)
print("2. INSERT rows (SQL's word for Create)")
print("=" * 60)

db.execute("INSERT INTO bags VALUES ('chanel-flap-001', 'Chanel', 'Classic Flap', 'like_new')")
db.execute("INSERT INTO bags VALUES ('lv-neverfull-001', 'Louis Vuitton', 'Neverfull MM', 'gently_used')")

# One bag, MANY price points — each row points back via bag_id:
db.execute("INSERT INTO price_points (bag_id, price, timestamp) VALUES ('chanel-flap-001', 9500.0, '2026-01-01')")
db.execute("INSERT INTO price_points (bag_id, price, timestamp) VALUES ('chanel-flap-001', 9800.0, '2026-02-01')")
db.execute("INSERT INTO price_points (bag_id, price, timestamp) VALUES ('lv-neverfull-001', 1800.0, '2026-01-15')")
print("  2 bags and 3 price points inserted.\n")

print("=" * 60)
print("3. SELECT — asking the table questions (SQL's Read)")
print("=" * 60)

print("  SELECT * FROM bags;")
for row in db.execute("SELECT * FROM bags"):
    print(f"    {row}")
print()

print("  SELECT * FROM bags WHERE brand = 'Chanel';")
for row in db.execute("SELECT * FROM bags WHERE brand = 'Chanel'"):
    print(f"    {row}")
print()

print("  All prices ever seen for the Chanel (one-to-many in action):")
print("  SELECT price, timestamp FROM price_points WHERE bag_id = 'chanel-flap-001';")
for row in db.execute("SELECT price, timestamp FROM price_points WHERE bag_id = 'chanel-flap-001'"):
    print(f"    {row}")
print()

print("=" * 60)
print("4. THE RULES PUSH BACK (this is why tables beat spreadsheets)")
print("=" * 60)

# Rule 1: a PRIMARY KEY must be unique. Try inserting a duplicate id:
try:
    db.execute("INSERT INTO bags VALUES ('chanel-flap-001', 'Fake', 'Dupe', 'new')")
except sqlite3.IntegrityError as error:
    print(f"  duplicate primary key  -> 💥 refused: {error}")

# Rule 2: a FOREIGN KEY must point at a row that EXISTS:
try:
    db.execute("INSERT INTO price_points (bag_id, price, timestamp) VALUES ('ghost-bag-999', 1.0, '2026-01-01')")
except sqlite3.IntegrityError as error:
    print(f"  price for ghost bag    -> 💥 refused: {error}")

print()
print("  Bad data stopped AT THE DOOR — no babysitting code needed.")
print("  (Phase 5.5's PostgreSQL is even stricter, e.g. about types.)")


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN
#
# 1. INSERT a third bag (your dream bag) and give it two price points.
#    Re-run and find them in the SELECT output.
# 2. Write a new query in section 3:
#       SELECT model FROM bags WHERE condition = 'gently_used'
#    PREDICT the output before you run it.
# 3. Try inserting a price_point with a missing price: copy one of the
#    INSERT lines in section 2 and replace the price number with the
#    word NULL (no quotes). Which rule refuses, and what does it say?
# 4. The big one — a JOIN stitches the two tables back together:
#       SELECT bags.brand, price_points.price
#       FROM bags JOIN price_points ON bags.id = price_points.bag_id
#    Add a loop that runs this and print each row. Each output row is
#    "a bag and one of its prices, side by side."
# ────────────────────────────────────────────────────────────────────
