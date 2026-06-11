"""
PLAYGROUND 05 — MVC: what goes where (and the swap trick)

Run me:   python3 playground/scripts/05_mvc.py
Primer:   docs/00-concepts.md, section 4

A complete Model-View-Controller app in ~60 lines — same layers as the
real project, miniature scale. The grand finale swaps out the model's
storage WITHOUT touching the controller, which is the whole reason MVC
exists. Watch for it.
"""

# ════════════════════════════════════════════════════════════════════
# MODEL — what the data IS and what it CAN DO. (real: app/models.py,
# app/store.py). Knows nothing about requests, JSON, or the web.
# ════════════════════════════════════════════════════════════════════

class Bag:
    def __init__(self, id, brand, model, prices):
        self.id = id
        self.brand = brand
        self.model = model
        self.prices = prices                # full price history

    def current_price(self):
        return self.prices[-1]              # most recent observation


class DictStore:
    """Keeps bags in a dict — like the real Phase 2 BagStore."""

    def __init__(self):
        self._bags = {}

    def add(self, bag):
        self._bags[bag.id] = bag

    def cheapest(self, n):
        ranked = sorted(self._bags.values(), key=lambda b: b.current_price())
        return ranked[:n]


# ════════════════════════════════════════════════════════════════════
# VIEW — the shape the outside world sees. (real: app/schemas.py)
# Picks WHICH fields go out and WHAT they're named. No logic.
# ════════════════════════════════════════════════════════════════════

def bag_response(bag):
    return {
        "id": bag.id,
        "label": f"{bag.brand} {bag.model}",          # renamed + combined!
        "current_price": bag.current_price(),
        # note what we DON'T send: the full price history stays private
    }


# ════════════════════════════════════════════════════════════════════
# CONTROLLER — the traffic cop. (real: the route functions in
# app/main.py). Calls the model, hands the result to the view.
# Notice: no business logic lives here. It only coordinates.
# ════════════════════════════════════════════════════════════════════

def get_cheapest_bags(store, n):
    """Handles 'GET /bags/cheapest?n=...'"""
    bags = store.cheapest(n)                    # 1. ask the MODEL
    return 200, [bag_response(b) for b in bags] # 2. shape with the VIEW


# ════════════════════════════════════════════════════════════════════
# Showtime
# ════════════════════════════════════════════════════════════════════

def fill(store):
    store.add(Bag("chanel-flap-001", "Chanel", "Classic Flap", [9500.0, 9800.0]))
    store.add(Bag("lv-neverfull-001", "Louis Vuitton", "Neverfull MM", [1800.0]))
    store.add(Bag("hermes-birkin-001", "Hermès", "Birkin 30", [22000.0, 23500.0]))


print("=" * 60)
print("REQUEST: GET /bags/cheapest?n=2   (using DictStore)")
print("=" * 60)

store = DictStore()
fill(store)
status, body = get_cheapest_bags(store, n=2)
print(f"  -> {status}")
for item in body:
    print(f"     {item}")

print()
print("=" * 60)
print("THE SWAP — a totally different storage, SAME controller")
print("=" * 60)


class ListStore:
    """Stores bags in a plain list instead of a dict. The internals are
    different — but it offers the SAME two methods, so nobody upstairs
    can tell the difference. In Phase 5.5 the 'different internals'
    will be an entire PostgreSQL database."""

    def __init__(self):
        self._bags = []

    def add(self, bag):
        self._bags.append(bag)

    def cheapest(self, n):
        return sorted(self._bags, key=lambda b: b.current_price())[:n]


store = ListStore()                            # <-- the ONLY changed line
fill(store)
status, body = get_cheapest_bags(store, n=2)   # untouched controller!
print(f"  -> {status}")
for item in body:
    print(f"     {item}")

print()
print("  Identical output, zero controller edits. THAT is MVC's payoff,")
print("  and you'll feel it for real in Phase 5.5 (BagStore -> SqlBagStore).")


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN
#
# 1. VIEW change: make `bag_response` also send "brand" as its own
#    field. Which layer did you touch? Did the model or controller
#    care?
# 2. The primer's question 5 (wrong currency label, right numbers) —
#    cause that bug here on purpose: make the view return
#    current_price as a dict {"price": ..., "currency": "EUR"}.
#    Notice you broke the OUTPUT without touching any logic.
# 3. MODEL change: add a method `price_change(self)` to Bag returning
#    last price minus first price, and add it to the view's output.
#    (This is literally Phase 1's exercise — sshh.)
# 4. CONTROLLER guardrail: in get_cheapest_bags, if n <= 0, return
#    (400, {"error": "n must be positive"}). Input-checking IS a
#    controller job — now each layer has earned its keep.
# ────────────────────────────────────────────────────────────────────
