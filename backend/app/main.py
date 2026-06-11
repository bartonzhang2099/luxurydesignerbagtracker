"""
Phase 4: FastAPI application.

Concepts: REST endpoints, path/query params, response models, error
handling with HTTPException.

Run with: `uvicorn app.main:app --reload` (from the `backend/` directory).
"""

from fastapi import FastAPI, HTTPException

from app.models import Bag
from app.schemas import BagCreate, BagResponse, PricePointResponse
from app.store import BagStore

app = FastAPI(title="Luxury Bag Price Tracker")
store = BagStore()

# TODO (Phase 5): on startup, load bags from data/sample_bags.json
# into `store` via `app.storage.load_store`, if the file exists.


def _to_response(bag: Bag) -> BagResponse:
    """Convert an internal `Bag` into the API's `BagResponse`.

    TODO:
    - Get `bag.current_price()`.
    - If it exists, build a `PricePointResponse` from it; otherwise use None.
    - Return a `BagResponse` built from the bag's fields plus
      `current_price`.
    """
    raise NotImplementedError


@app.get("/bags", response_model=list[BagResponse])
def list_bags() -> list[BagResponse]:
    """List every bag in the store.

    TODO: return `[_to_response(b) for b in store.all()]`.
    """
    raise NotImplementedError


@app.get("/bags/cheapest", response_model=list[BagResponse])
def cheapest_bags(n: int = 5) -> list[BagResponse]:
    """Return the `n` cheapest bags by current price.

    Note: this route must be declared before `/bags/{bag_id}`,
    otherwise FastAPI will try to match "cheapest" as a `bag_id`.

    TODO: use `store.cheapest(n)` and map with `_to_response`.
    """
    raise NotImplementedError


@app.get("/bags/{bag_id}", response_model=BagResponse)
def get_bag(bag_id: str) -> BagResponse:
    """Return a single bag, or 404 if it doesn't exist.

    TODO:
    - Look up the bag via `store.get(bag_id)`.
    - If `None`, raise `HTTPException(status_code=404, detail="Bag not found")`.
    - Otherwise return `_to_response(bag)`.
    """
    raise NotImplementedError


@app.post("/bags", response_model=BagResponse, status_code=201)
def create_bag(payload: BagCreate) -> BagResponse:
    """Create a new bag listing.

    TODO:
    - Build a `Bag` from `payload`'s fields (everything except
      `price`/`currency`).
    - If `payload.price is not None`, call
      `bag.add_price(payload.price, payload.currency)`.
    - Add the bag to `store`.
    - Return `_to_response(bag)`.
    """
    raise NotImplementedError
