"""
PLAYGROUND 06 — One request, narrated end to end

Run me:   python3 playground/scripts/06_request_flow.py
Primer:   docs/00-concepts.md, section 5

The primer lists the 6 steps a request takes through the finished
project. This script EXECUTES those steps and narrates each one as it
happens. Same layers as playground 05, now with the play-by-play.
"""

import json

# ── the cast (tiny versions of the real files) ──────────────────────

BAGS = {   # the model's data (real: BagStore / the database)
    "chanel-flap-001": {"brand": "Chanel", "model": "Classic Flap", "prices": [9500.0, 9800.0]},
    "lv-neverfull-001": {"brand": "Louis Vuitton", "model": "Neverfull MM", "prices": [1800.0]},
    "hermes-birkin-001": {"brand": "Hermès", "model": "Birkin 30", "prices": [22000.0]},
    "coach-tabby-001": {"brand": "Coach", "model": "Tabby 26", "prices": [450.0]},
}


def store_cheapest(n):                      # MODEL  (real: app/store.py)
    ranked = sorted(BAGS.items(), key=lambda item: item[1]["prices"][-1])
    return ranked[:n]


def bag_response(bag_id, bag):              # VIEW   (real: app/schemas.py)
    return {"id": bag_id,
            "label": f"{bag['brand']} {bag['model']}",
            "current_price": bag["prices"][-1]}


# ── the narrated journey ─────────────────────────────────────────────

raw_request = "GET /bags/cheapest?n=2"

print(f'A request knocks:  "{raw_request}"')
print()

print("STEP 1 — the request arrives at the server")
print("         (real life: FastAPI in app/main.py is listening)")
method, rest = raw_request.split(" ")
path, query = rest.split("?")
print(f"         method={method!r}  path={path!r}  query={query!r}")
print()

print("STEP 2 — the server matches the path to a CONTROLLER function")
print("         and parses the query parameter into a real int")
n = int(query.removeprefix("n="))           # "n=2" -> 2
print(f"         matched: cheapest_bags(n={n})   (n is now an int, not text)")
print()

print("STEP 3 — the controller calls the MODEL: store.cheapest(2)")
results = store_cheapest(n)
print(f"         the model went looking through {len(BAGS)} bags...")
print()

print("STEP 4 — the model returns the 2 cheapest Bag objects (R in CRUD)")
for bag_id, bag in results:
    print(f"         {bag_id}  (current price ${bag['prices'][-1]})")
print()

print("STEP 5 — the controller passes each Bag through the VIEW")
shaped = [bag_response(bag_id, bag) for bag_id, bag in results]
print(f"         full price history hidden, fields renamed:")
for item in shaped:
    print(f"         {item}")
print()

print("STEP 6 — the server turns that into JSON text + status 200")
print("         and sends it back over the wire:")
print()
print("HTTP 200 OK")
print(json.dumps(shaped, indent=2, ensure_ascii=False))
print()
print("Six steps, four concepts (API, CRUD, table, MVC), one request.")
print("Every phase you're about to build is one piece of this pipeline.")


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN
#
# 1. Change raw_request to "GET /bags/cheapest?n=3" — re-run. Which
#    steps printed differently? Which didn't change at all?
# 2. Set n to a number BIGGER than the number of bags (n=10). Does it
#    crash or cope? Find the line that decides.
# 3. Break step 2 on purpose: raw_request = ".../cheapest?n=two".
#    Read the crash. In real FastAPI this exact mistake returns a 422
#    error to the caller instead of crashing — Phase 4 will show you.
# 4. Out loud, no peeking: which file in the REAL app/ folder plays
#    each role? (Steps 1-2: ____, step 3-4: ____, step 5: ____.)
#    Answers are in the primer's MVC diagram.
# ────────────────────────────────────────────────────────────────────
