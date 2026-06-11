"""
PLAYGROUND 03 — CRUD: the four verbs under every app

Run me:   python3 playground/scripts/03_crud.py
Primer:   docs/00-concepts.md, section 2

Create, Read, Update, Delete — on a plain Python dict. This is a
hand-rolled mini version of the `BagStore` you'll build for real in
Phase 2 (and expose over an API in Phase 4, and back with PostgreSQL
in Phase 5.5 — same four verbs every time).
"""

# Our entire "database" for today — one dict, mapping id -> bag.
store = {}


def show_store(moment):
    print(f"  store {moment}: {len(store)} bag(s)")
    for bag_id, bag in store.items():
        print(f"    {bag_id}: {bag['brand']} {bag['model']} — ${bag['price']}")
    print()


print("=" * 60)
print("C — CREATE  ('add a new one')")
print("=" * 60)

store["chanel-flap-001"] = {"brand": "Chanel", "model": "Classic Flap", "price": 9500.0}
store["lv-neverfull-001"] = {"brand": "Louis Vuitton", "model": "Neverfull MM", "price": 1800.0}
store["hermes-birkin-001"] = {"brand": "Hermès", "model": "Birkin 30", "price": 22000.0}

show_store("after 3 creates")

print("=" * 60)
print("R — READ  ('show me')")
print("=" * 60)

# Read ONE, by its id:
print(f"  get one:  {store['lv-neverfull-001']}")

# Read with a question attached ("which bags are under $5000?"):
cheap = [bag for bag in store.values() if bag["price"] < 5000]
print(f"  filtered: {cheap}")
print()

print("=" * 60)
print("U — UPDATE  ('change it')")
print("=" * 60)

print(f"  Birkin before: ${store['hermes-birkin-001']['price']}")
store["hermes-birkin-001"]["price"] = 23500.0     # resale prices move!
print(f"  Birkin after:  ${store['hermes-birkin-001']['price']}")
print()

print("=" * 60)
print("D — DELETE  ('remove it')")
print("=" * 60)

del store["lv-neverfull-001"]
show_store("after deleting the Neverfull")

print("=" * 60)
print("THE TRAP EVERY BEGINNER HITS ONCE")
print("=" * 60)

# Reading (or deleting) an id that isn't there CRASHES with a KeyError:
try:
    store["gucci-jackie-001"]
except KeyError:
    print("  store['gucci-jackie-001']     -> 💥 KeyError!")

# The polite alternative — .get() returns None instead of crashing:
print(f"  store.get('gucci-jackie-001') -> {store.get('gucci-jackie-001')}")
print()
print("  Remember this pair. In Phase 2, BagStore.get() must return")
print("  None for unknown ids — now you know which dict tool does that.")


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN
#
# 1. CREATE your own dream bag in the store, then READ it back.
# 2. UPDATE the Chanel's price to 9999.0 and re-run.
# 3. Before running anything: what do you PREDICT happens if you
#    delete 'lv-neverfull-001' a SECOND time (add a second `del` line
#    right after the first)? Run it. Were you right? Remove it again.
# 4. Map it back to real life: on Instagram, what are one example each
#    of C, R, U and D? Say them out loud.
# 5. Stretch: write a function `cheapest(store)` that returns the
#    lowest-priced bag dict. (Hint: loop over store.values() and keep
#    the best one seen so far.) Phase 3 asks for exactly this, with
#    a fancier data structure.
# ────────────────────────────────────────────────────────────────────
