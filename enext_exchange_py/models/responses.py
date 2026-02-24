from dataclasses import dataclass
from datetime import datetime

__all__ = ["DetailedQuote", "Quote", "EncryptedResponse", "Price", "Factsheet"]


@dataclass(frozen=True)
class EncryptedResponse:
    ct: str
    s: str
    iv: str


@dataclass(frozen=True)
class Price:
    value: float
    currency: str | None = None


@dataclass(frozen=True)
class DetailedQuote:
    name: str | None = None
    symbol: str | None = None
    last_traded_price: Price | None = None
    last_traded_time: datetime | None = None
    since_open_percentage: float | None = None
    since_previous_close_percentage: float | None = None


@dataclass(frozen=True)
class Quote:
    time: datetime
    price: float
    volume: int


@dataclass(frozen=True)
class Factsheet:
    isin: str | None = None
    code: str | None = None
    instrument_type: str | None = None
    instrument_sub_type: str | None = None
    segment: str | None = None
    trading_mode: str | None = None
    trading_group: str | None = None
    trading_currency: str | None = None
    quantity_notation: str | None = None
    shares_outstanding: int | None = None
    tick_size: str | None = None
