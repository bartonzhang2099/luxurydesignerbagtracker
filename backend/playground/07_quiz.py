"""
PLAYGROUND 07 — Interactive check-yourself quiz

Run me:   python3 playground/07_quiz.py
Primer:   docs/00-concepts.md, "Check yourself"

The primer's 6 questions, one at a time. Type your answer in your own
words (or say it out loud and just press Enter) — then the script shows
the reference answer so you can compare. Nobody is grading you; the
point is noticing which ideas feel solid and which need a re-read.
"""

QUESTIONS = [
    ("In the restaurant analogy, what are the waiter, the kitchen, "
     "and the menu?",
     "Waiter = frontend, kitchen = backend, menu = API.",
     "§1"),

    ("You favorite a bag on a resale app. Which CRUD letter is that? "
     "You scroll the listings — which letter?",
     "Favoriting = Create (a new 'favorite' record) — Update is also a "
     "defensible answer. Scrolling = Read.",
     "§2"),

    ("Why does price_points get its own table instead of storing "
     "prices inside the bags table?",
     "A bag has an unknown, growing number of price observations — "
     "'many of a thing' becomes rows in a separate table pointing back "
     "at the owner via a foreign key.",
     "§3"),

    ("What's the difference between a primary key and a foreign key?",
     "Primary key: uniquely identifies a row in its OWN table. Foreign "
     "key: a column that POINTS AT another table's primary key.",
     "§3"),

    ("A bug makes GET /bags show the right prices but label them all "
     "'EUR' instead of 'USD'. Model, view, or controller bug?",
     "View — the data is right, the outgoing shape/label is wrong "
     "(schemas.py / the response-building code). You caused this exact "
     "bug on purpose in playground 05, YOUR TURN #2!",
     "§4"),

    ("Why can main.py stay almost unchanged when storage moves from a "
     "Python dict to PostgreSQL?",
     "The controller only calls model methods like cheapest(n) and "
     "never cares how they're implemented — both stores offer the same "
     "methods. You performed this swap yourself in playground 05.",
     "§4-5"),
]


print("=" * 60)
print("PHASE 0 CHECK-YOURSELF QUIZ — 6 questions, zero pressure")
print("=" * 60)
print("Answer in your own words, or answer out loud and press Enter.")
print()

needs_review = []

for number, (question, answer, section) in enumerate(QUESTIONS, start=1):
    print(f"Q{number}. {question}")
    print()
    input("    your answer> ")
    print()
    print(f"    📖 reference answer: {answer}")
    print()
    verdict = input("    Did you basically have it? [y/n] > ").strip().lower()
    if verdict != "y":
        needs_review.append((number, section))
    print()
    print("-" * 60)
    print()

print("=" * 60)
if not needs_review:
    print("6/6 — you're ready. Go start Phase 1: docs/01-models.md 🎉")
else:
    print(f"You nailed {6 - len(needs_review)}/6. Worth a re-read:")
    for number, section in needs_review:
        print(f"  - Q{number}: docs/00-concepts.md {section}")
    print("Re-read those sections (and replay the matching playground")
    print("script), then run me again. Repetition is the whole trick.")
print("=" * 60)


# ────────────────────────────────────────────────────────────────────
# ✏️  YOUR TURN (yes, even the quiz is editable)
#
# 1. Add a 7th question of your own — something YOU found confusing —
#    with your own reference answer. Teaching-yourself-by-writing-the-
#    question is a sneaky-effective study trick.
# 2. Notice this script uses everything from playground 00: a list of
#    tuples, a for loop, f-strings, if/else. Reading code you already
#    understand is how it starts to feel like home.
# ────────────────────────────────────────────────────────────────────
