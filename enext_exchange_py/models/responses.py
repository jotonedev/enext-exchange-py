from dataclasses import dataclass
from datetime import datetime

__all__ = [
    "DetailedQuote",
    "Quote",
    "EncryptedResponse",
    "Price"
]

@dataclass(frozen=True)
class EncryptedResponse:
    ct: str
    s: str
    iv: str

@dataclass(frozen=True)
class Price:
    value: float
    currency: str

@dataclass(frozen=True)
class DetailedQuote:
    name: str | None = None
    symbol: str | None = None
    last_traded_price: Price | None = None
    last_traded_time: datetime | None = None
    since_open_percentage: float | None = None
    since_previous_close_percentage: float | None = None
    valuation_close_price: Price | None = None
    valuation_close_time: datetime | None = None

@dataclass(frozen=True)
class Quote:
    time: datetime
    price: Price
    volume: int
