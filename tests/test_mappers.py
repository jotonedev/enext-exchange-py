import datetime

from enext_exchange_py.mappers import time_str_to_datetime

def test__map_page_to_detailed_quote():
    assert False


def test__map_page_to_factsheet():
    assert False


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
