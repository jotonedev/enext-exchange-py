import re

from parsel import Selector

from datetime import datetime
from dateutil import tz


__all__ = [
    "time_str_to_datetime",
    "map_page_to_factsheet",
    "map_page_to_detailed_quote"
]

from enext_exchange_py.models import DetailedQuote, Price

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
    "€": "EUR"
}

def time_str_to_datetime(time_str: str) -> datetime:
    time_str = re.sub(r'[^A-Z\d/:]', ' ', time_str)
    time_str = re.sub(r'\s+', ' ', time_str)
    time_str = time_str.strip()

    parts = time_str.rsplit(' ', 1)
    dt_part = parts[0]
    tz_part = parts[1]

    date = datetime.strptime(dt_part, "%d/%m/%Y %H:%M")

    timezone = TZ_MAPPING.get(tz_part)

    date = date.replace(tzinfo=timezone)
    return date


def map_page_to_factsheet(page: Selector):
    return (
        page.css(".factsheet-table-row-1-1").get()
    )


def map_page_to_detailed_quote(page: Selector):
    name = page.css("h1").css("strong::text").get()
    if name is not None:
        name = name.strip()

    symbol = page.css("div.enx-symbol-top-custom::text").get()
    if symbol is not None:
        symbol = symbol.strip()

    last_traded_price_currency = page.css("#header-instrument-currency::text").get()
    if last_traded_price_currency is not None:
        last_traded_price_currency = last_traded_price_currency.strip()
        last_traded_price_currency = CURRENCY_MAPPING.get(last_traded_price_currency, last_traded_price_currency)

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
        value = re.sub(r'\s+', ' ', value).strip()
        value = re.sub(r'[^0-9.]', '', value)
        if text == "Since Open":
            since_open_percentage = float(value)
        elif text == "Since Previous Close":
            since_previous_close_percentage = float(value)

    valuation_close_price_currency = page.css("#col-header-instrument-currency::text").get()
    if valuation_close_price_currency is not None:
        valuation_close_price_currency = valuation_close_price_currency.strip()
        valuation_close_price_currency = CURRENCY_MAPPING.get(valuation_close_price_currency, valuation_close_price_currency)

    valuation_close_price = page.css("#col-header-instrument-price::text").get()
    if valuation_close_price is not None:
        valuation_close_price = float(valuation_close_price.strip())
        valuation_close_price = Price(valuation_close_price, valuation_close_price_currency)

    valuation_close_time = page.css("#col-header-instrument-closing-price-date-time::text").get()
    if valuation_close_time is not None:
        valuation_close_time = time_str_to_datetime(valuation_close_time)

    return DetailedQuote(
        name=name,
        symbol=symbol,
        last_traded_price=last_traded_price,
        last_traded_time=last_traded_time,
        since_open_percentage=since_open_percentage,
        since_previous_close_percentage=since_previous_close_percentage,
        valuation_close_price=valuation_close_price,
        valuation_close_time=valuation_close_time,
    )