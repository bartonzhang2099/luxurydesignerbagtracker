"""
PLAYGROUND 01 — JSON: how programs mail data to each other

Run me:   python3 playground/scripts/01_json.py
Primer:   docs/00-concepts.md, section 1 (the JSON part)

A Python dict lives inside ONE running program. JSON is that same data
flattened into plain text, so it can travel — over the internet, into a
file — and be rebuilt on the other side. Phase 4's API will speak JSON,
and Phase 5 saves bags to a .json file. This is that, in miniature.
"""

import json   # Python's built-in JSON translator

print("=" * 60)
print("1. PYTHON DICT  ->  JSON TEXT   (json.dumps = 'dump to string')")
print("=" * 60)

bag = {
    "id": "chanel-flap-001",
    "brand": "Chanel",
    "price": 9500.0,
    "is_available": True,
    "previous_owner": None,
    "tags": ["classic", "caviar-leather"],
}

as_text = json.dumps(bag, indent=2)   # indent=2 just makes it pretty

print(f"type before: {type(bag)}")
print(f"type after:  {type(as_text)}   <-- it's just text now!")
print()
print(as_text)
print()
print("Spot the translations: True -> true, None -> null.")
print("Curly braces = an object. Square brackets = a list.")
print("That really is ~90% of all JSON you'll ever read.")

print()
print("=" * 60)
print("2. JSON TEXT  ->  PYTHON DICT   (json.loads = 'load from string')")
print("=" * 60)

# Pretend this string just arrived over the internet from a resale site:
incoming = '{"id": "lv-neverfull-001", "brand": "Louis Vuitton", "price": 1800.0}'

parsed = json.loads(incoming)

print(f"raw text:           {incoming}")
print(f"after json.loads:   {parsed}")
print(f"now I can do dict things:  parsed['brand'] = {parsed['brand']}")

print()
print("=" * 60)
print("3. BROKEN JSON — what happens when the text is malformed?")
print("=" * 60)

broken = '{"id": "hermes-birkin-001", "price": }'   # value missing!

try:
    json.loads(broken)
except json.JSONDecodeError as error:
    print(f"Python refused, saying: {error}")
    print("APIs face this constantly — never trust incoming text blindly.")


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN
#
# 1. Add "color": "Black Caviar" to the `bag` dict and re-run. Find it
#    in the JSON output.
# 2. JSON inside JSON: give `bag` a key "current_price" whose value is
#    another dict: {"price": 9500.0, "currency": "USD"}. Re-run — this
#    nested shape is exactly what the primer's example response shows.
# 3. In section 2, edit `incoming` to add a "color" field — remember
#    JSON needs double quotes around keys AND text values.
# 4. Break it on purpose: remove one comma from `incoming`, run, and
#    read the error. Does the error tell you WHERE the problem is?
# ────────────────────────────────────────────────────────────────────
