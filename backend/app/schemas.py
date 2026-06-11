"""
Phase 4: Pydantic schemas for the API.

Concepts: request/response validation with Pydantic, separating your
internal models (`app.models.Bag`) from your API's "shape".
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models import BagCondition


class BagCreate(BaseModel):
    """Request body for `POST /bags`.

    `price`/`currency` are optional - if provided, an initial
    `PricePoint` should be recorded for the new bag.
    """

    id: str
    brand: str
    model: str
    color: str
    condition: BagCondition
    source: str
    price: Optional[float] = None
    currency: str = "USD"


class PricePointResponse(BaseModel):
    price: float
    currency: str
    timestamp: datetime


class BagResponse(BaseModel):
    """Response shape for a bag, including its latest price."""

    id: str
    brand: str
    model: str
    color: str
    condition: BagCondition
    source: str
    current_price: Optional[PricePointResponse] = None
