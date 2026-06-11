"""
PLAYGROUND 02 — A fake backend you can poke (waiter, kitchen, menu)

Run me:   python3 playground/scripts/02_api_kitchen.py
Primer:   docs/00-concepts.md, section 1

A real API call crosses the internet. But the IDEA needs no internet:
the frontend sends (method, path), the backend looks at them, and
returns (status_code, data). Below, `fake_backend` is the kitchen —
one ordinary Python function — and the calls at the bottom are you,
playing the waiter. In Phase 4, FastAPI replaces this function with
the real thing; the shape of the conversation stays identical.
"""

# The kitchen's pantry — all the data the backend "owns":
BAGS = {
    "chanel-flap-001": {"brand": "Chanel", "model": "Classic Flap", "price": 9500.0},
    "lv-neverfull-001": {"brand": "Louis Vuitton", "model": "Neverfull MM", "price": 1800.0},
    "hermes-birkin-001": {"brand": "Hermès", "model": "Birkin 30", "price": 22000.0},
}


def fake_backend(method, path, body=None):
    """The entire 'kitchen'. Takes a request, returns (status_code, data).

    Compare each branch below with the primer's menu table — it's the
    same four endpoints.
    """
    # "show me all the bags"
    if method == "GET" and path == "/bags":
        return 200, list(BAGS.values())

    # "show me ONE bag" — e.g. GET /bags/chanel-flap-001
    if method == "GET" and path.startswith("/bags/"):
        bag_id = path.removeprefix("/bags/")   # the part after /bags/
        if bag_id in BAGS:
            return 200, BAGS[bag_id]
        return 404, {"error": f"no bag with id '{bag_id}'"}   # not found!

    # "here's a new bag, please save it"
    if method == "POST" and path == "/bags":
        if body is None or "id" not in body:
            return 400, {"error": "you must send a bag with an 'id'"}
        BAGS[body["id"]] = {k: v for k, v in body.items() if k != "id"}
        return 201, {"saved": body["id"]}      # 201 = created

    # Anything not on the menu:
    return 404, {"error": f"unknown endpoint: {method} {path}"}


def request(method, path, body=None):
    """You, the waiter: carry an order to the kitchen, print the reply."""
    status, data = fake_backend(method, path, body)
    print(f"  {method} {path}")
    print(f"  -> {status}  {data}")
    print()


print("=" * 60)
print("THE MENU IN ACTION")
print("=" * 60)
print()

request("GET", "/bags")                       # read everything   -> 200
request("GET", "/bags/chanel-flap-001")       # read one          -> 200
request("GET", "/bags/gucci-jackie-001")      # doesn't exist     -> 404
request("POST", "/bags",                      # create one        -> 201
        body={"id": "coach-tabby-001", "brand": "Coach",
              "model": "Tabby 26", "price": 450.0})
request("GET", "/bags/coach-tabby-001")       # ...and now it exists!
request("DELETE", "/bags/chanel-flap-001")    # not on the menu   -> 404

print("Status codes you just saw:  200 OK · 201 created · 404 not found")
print("(500 = 'kitchen on fire' only happens when the BACKEND has a bug.)")


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN
#
# 1. Before re-running: PREDICT the status code of
#    GET /bags/hermes-birkin-001 — then add that request() call at the
#    bottom and check yourself.
# 2. Send a bad POST: request("POST", "/bags", body={"brand": "Dior"})
#    (no "id"). What status comes back, and why?
# 3. Add a new endpoint to fake_backend: GET /bags/count should return
#    200 and {"count": len(BAGS)}. ⚠️ Order matters: put your branch
#    ABOVE the startswith("/bags/") branch — otherwise that branch
#    catches it first and thinks "count" is a bag id. (Try it below
#    the branch first and watch that exact bug happen!)
# 4. Stretch: support DELETE /bags/{id} — remove the bag from BAGS and
#    return 200. That's the D in CRUD, one script early.
# ────────────────────────────────────────────────────────────────────
