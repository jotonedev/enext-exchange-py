import re
from datetime import datetime

from dateutil import tz
from parsel import Selector

from enext_exchange_py.models import DetailedQuote, Factsheet, Price

__all__ = ["time_str_to_datetime", "map_page_to_factsheet", "map_page_to_detailed_quote"]


# TODO: Replace this with a proper mapping, currently zoneinfo/datetime it is limited by the timezone data available on the system
TZ_MAPPING = {
    "UTC": tz.gettz("UTC"),
    "GMT": tz.gettz("Europe/London"),
    "BST": tz.gettz("Europe/London"),
    "CET": tz.gettz("Europe/Berlin"),
    "CEST": tz.gettz("Europe/Berlin"),
    "EET": tz.gettz("Europe/Helsinki"),
    "EEST": tz.gettz("Europe/Helsinki"),
}

CURRENCY_MAPPING = {
    "€": "EUR",
    "$": "USD",
}


def time_str_to_datetime(time_str: str) -> datetime:
    time_str = re.sub(r"[^A-Z\d/:]", " ", time_str)
    time_str = re.sub(r"\s+", " ", time_str)
    time_str = time_str.strip()

    parts = time_str.rsplit(" ", 1)
    dt_part = parts[0]
    tz_part = parts[1]

    date = datetime.strptime(dt_part, "%d/%m/%Y %H:%M")

    timezone = TZ_MAPPING.get(tz_part)

    date = date.replace(tzinfo=timezone)
    return date


def map_page_to_factsheet(page: Selector) -> Factsheet:
    table = page.css("table.table")

    raw_data = {}
    for row in table.css("tbody").css("tr"):
        cells = row.css("td::text").getall()
        if len(cells) != 2:
            continue
        key = cells[0].strip()
        value = cells[1].strip()

        if key is not None and value is not None:
            raw_data[key] = value.strip()

    data = {}
    if raw_data.get("ISIN") is not None:
        data["isin"] = raw_data["ISIN"].upper()

    if raw_data.get("Euronext Code") is not None:
        data["code"] = raw_data["Euronext Code"].upper()

    if raw_data.get("Intrument type") is not None:
        data["instrument_type"] = raw_data["Intrument type"]

    if raw_data.get("Intrument Sub-type") is not None:
        data["instrument_sub_type"] = raw_data["Intrument Sub-type"]

    if raw_data.get("Segment") is not None:
        data["segment"] = raw_data["Segment"]

    if raw_data.get("Trading Mode") is not None:
        data["trading_mode"] = raw_data["Trading Mode"]

    if raw_data.get("Trading Group") is not None:
        data["trading_group"] = raw_data["Trading Group"]

    if raw_data.get("Trading Currency") is not None:
        data["trading_currency"] = raw_data["Trading Currency"].upper()

    if raw_data.get("Quantity notation") is not None:
        data["quantity_notation"] = raw_data["Quantity notation"]

    if raw_data.get("Shared outstanding") is not None:
        data["shares_outstanding"] = raw_data["Shared outstanding"]

    if raw_data.get("Tick size") is not None:
        data["tick_size"] = raw_data["Tick size"]

    return Factsheet(**data)


def map_page_to_detailed_quote(page: Selector) -> DetailedQuote:
    name = page.css("h1").css("strong::text").get()
    if name is not None:
        name = name.strip()

    symbol = page.css("div.enx-symbol-top-custom::text").get()
    if symbol is not None:
        symbol = symbol.strip()

    last_traded_price_currency = page.css("#header-instrument-currency::text").get()
    if last_traded_price_currency is not None:
        last_traded_price_currency = last_traded_price_currency.strip()
        last_traded_price_currency = CURRENCY_MAPPING.get(
            last_traded_price_currency, last_traded_price_currency
        )

    last_traded_price = page.css("#header-instrument-price::text").get()
    if last_traded_price is not None:
        last_traded_price = float(last_traded_price.strip())
        last_traded_price = Price(last_traded_price, last_traded_price_currency)

    last_traded_time = page.css("div.last-price-date-time::text").get()
    if last_traded_time is not None:
        last_traded_time = time_str_to_datetime(last_traded_time)

    since_open_percentage = None
    since_previous_close_percentage = None
    data_header = page.css("div.data-header__row")
    for row in data_header.css("div.col"):
        text = row.css("div.data-12::text").get()
        if text is None:
            continue
        value = data_header.css("span.data-24::text").get()
        if value is None:
            continue
        value = re.sub(r"\s+", " ", value).strip()
        value = re.sub(r"[^0-9.]", "", value)
        if text == "Since Open":
            since_open_percentage = float(value)
        elif text == "Since Previous Close":
            since_previous_close_percentage = float(value)

    return DetailedQuote(
        name=name,
        symbol=symbol,
        last_traded_price=last_traded_price,
        last_traded_time=last_traded_time,
        since_open_percentage=since_open_percentage,
        since_previous_close_percentage=since_previous_close_percentage,
    )
