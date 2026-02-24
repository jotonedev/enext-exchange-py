import datetime

import parsel

from enext_exchange_py.mappers import (
    map_page_to_detailed_quote,
    map_page_to_factsheet,
    time_str_to_datetime,
)
from enext_exchange_py.models import DetailedQuote, Factsheet


def test__map_empty_page_to_detailed_quote():
    empty_page = parsel.Selector("")
    quote = map_page_to_detailed_quote(empty_page)

    assert isinstance(quote, DetailedQuote)
    assert quote.name is None
    assert quote.symbol is None
    assert quote.last_traded_price is None
    assert quote.last_traded_time is None
    assert quote.since_open_percentage is None
    assert quote.since_previous_close_percentage is None


def test__map_empty_page_to_factsheet():
    empty_page = parsel.Selector("")
    factsheet = map_page_to_factsheet(empty_page)

    assert isinstance(factsheet, Factsheet)
    assert factsheet.isin is None
    assert factsheet.code is None
    assert factsheet.instrument_type is None
    assert factsheet.instrument_sub_type is None
    assert factsheet.segment is None
    assert factsheet.trading_mode is None
    assert factsheet.trading_group is None
    assert factsheet.trading_currency is None
    assert factsheet.quantity_notation is None
    assert factsheet.shares_outstanding is None
    assert factsheet.tick_size is None


def test_time_str_to_datetime_tz_cet():
    time_str = "\t\t\t\t20/02/2026\t\t\t\t - 09:35 \n\t\t CET\n\t\t\t"
    date = time_str_to_datetime(time_str)
    assert date.year == 2026
    assert date.month == 2
    assert date.day == 20
    assert date.hour == 9
    assert date.minute == 35
    assert date.tzinfo is not None

    assert date.tzinfo.tzname(date) == "CET"
    assert date.tzinfo.utcoffset(date) == datetime.timedelta(hours=1)
