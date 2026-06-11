"""
Phase 5 tests: run with `pytest -v tests/test_storage.py`

Implement `app/storage.py` until these pass.
"""

from datetime import datetime
from pathlib import Path

from app.models import Bag, BagCondition
from app.storage import load_store, save_store
from app.store import BagStore


def test_save_and_load_round_trip(tmp_path: Path):
    store = BagStore()

    bag = Bag(
        id="b1",
        brand="Chanel",
        model="Classic Flap Medium",
        color="Black",
        condition=BagCondition.LIKE_NEW,
        source="test",
    )
    bag.add_price(9500.0, "USD", timestamp=datetime(2026, 1, 1, 9, 0, 0))
    bag.add_price(8900.0, "USD", timestamp=datetime(2026, 2, 1, 9, 0, 0))
    store.add(bag)

    out_path = tmp_path / "bags.json"
    save_store(store, out_path)

    assert out_path.exists()

    loaded = load_store(out_path)
    loaded_bag = loaded.get("b1")

    assert loaded_bag is not None
    assert loaded_bag.brand == "Chanel"
    assert loaded_bag.model == "Classic Flap Medium"
    assert loaded_bag.color == "Black"
    assert loaded_bag.condition == BagCondition.LIKE_NEW

    assert len(loaded_bag.price_history) == 2
    assert loaded_bag.price_history[0].timestamp == datetime(2026, 1, 1, 9, 0, 0)
    assert loaded_bag.current_price().price == 8900.0


def test_load_sample_bags():
    sample_path = Path(__file__).resolve().parents[1] / "data" / "sample_bags.json"

    store = load_store(sample_path)

    chanel_bags = store.by_brand("Chanel")
    assert len(chanel_bags) == 2

    cheapest = store.cheapest(1)
    assert cheapest[0].id == "coach-tabby-001"
