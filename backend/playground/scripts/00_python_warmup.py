"""
PLAYGROUND 00 — Python warm-up (run me first!)

Run me:   python3 playground/scripts/00_python_warmup.py

Five tiny ideas — variables, lists, dictionaries, loops, functions —
that every later script (and the whole project) is built from.
Read the code AND the output side by side.
"""

print("=" * 60)
print("1. VARIABLES — a name stuck on a value")
print("=" * 60)

brand = "Chanel"            # text  (called a "string", or str)
price = 9500.0              # a decimal number (a "float")
year = 2026                 # a whole number (an "int")
is_sold_out = False         # True or False (a "bool")

# An f-string lets you drop variables into text with {curly braces}:
print(f"A {brand} bag costs ${price} in {year}. Sold out? {is_sold_out}")

print()
print("=" * 60)
print("2. LISTS — an ordered row of values")
print("=" * 60)

prices = [9500.0, 9800.0, 9650.0]   # square brackets = list

print(f"all prices:        {prices}")
print(f"first price:       {prices[0]}")    # counting starts at 0!
print(f"last price:        {prices[-1]}")   # -1 means 'from the end'
print(f"how many prices:   {len(prices)}")

prices.append(9900.0)                       # add to the end
print(f"after append:      {prices}")

print()
print("=" * 60)
print("3. DICTIONARIES — values looked up by name, not position")
print("=" * 60)

# A dict maps a KEY to a VALUE. Like a contacts app: name -> number.
bag = {
    "id": "chanel-flap-001",
    "brand": "Chanel",
    "model": "Classic Flap Medium",
    "price": 9500.0,
}

print(f"the whole dict:    {bag}")
print(f"just the brand:    {bag['brand']}")   # look up by key

bag["color"] = "Black Caviar"                 # add a new key
bag["price"] = 9800.0                         # overwrite an existing one
print(f"after editing:     {bag}")

print()
print("=" * 60)
print("4. LOOPS — do something to every item")
print("=" * 60)

bags = ["chanel-flap-001", "lv-neverfull-001", "hermes-birkin-001"]

for bag_id in bags:                  # 'bag_id' takes each value in turn
    if bag_id.startswith("chanel"):  # 'if' = only sometimes
        print(f"  {bag_id}   <-- it's a Chanel!")
    else:
        print(f"  {bag_id}")

print()
print("=" * 60)
print("5. FUNCTIONS — a recipe with a name")
print("=" * 60)

# 'def' defines a function: inputs in parentheses, result after 'return'.
def price_drop(old_price, new_price):
    """How many dollars cheaper did it get?"""
    return old_price - new_price

drop = price_drop(9800.0, 9500.0)    # 'calling' the function
print(f"price_drop(9800, 9500) = {drop}")
print(f"price_drop(100, 250)   = {price_drop(100.0, 250.0)}  (negative = it got pricier)")


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN  (edit above, re-run, watch the output change)
#
# 1. In section 1, change `brand` to your dream bag's brand and re-run.
# 2. In section 2, print `prices[1]`. Before running: which number do
#    you PREDICT comes out? (Remember: counting starts at 0.)
# 3. In section 3, try printing `bag['size']` — a key that doesn't
#    exist. Run it, read the error message (KeyError), then remove it
#    again. Now you've met your first error — it won't be the last,
#    and that's fine.
# 4. In section 5, write your own function `is_expensive(price)` that
#    returns True if price > 5000, and print what it says for 9500
#    and for 120.
# ────────────────────────────────────────────────────────────────────
