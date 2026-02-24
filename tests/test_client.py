import datetime
import unittest

import pytest

from enext_exchange_py.client import ExchangeClient
from enext_exchange_py.models import DetailedQuote, Quote


@pytest.mark.asyncio
class TestClient(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        self.client = ExchangeClient()
        super().__init__(*args, **kwargs)

    async def test__get_detailed_quote(self):
        resp = await self.client.get_detailed_quote("LU0290358497-ETFP")

        assert isinstance(resp, DetailedQuote)
        assert resp.last_traded_price is not None
        assert resp.last_traded_price.value >= 0
        assert isinstance(resp.last_traded_time, datetime.datetime)
        assert resp.since_open_percentage is not None
        assert resp.since_previous_close_percentage is not None

    async def test__get_intraday_quotes(self):
        resp = self.client.get_intraday_quotes("LU0290358497-ETFP")
        first_value = await anext(resp)

        assert isinstance(first_value, Quote)
        assert isinstance(first_value.time, datetime.datetime)
        assert first_value.price > 0
        assert first_value.volume >= 0

    async def test__get_historical_quotes(self):
        resp = self.client.get_historical_quotes("LU0290358497-ETFP")
        first_value = await anext(resp)

        assert isinstance(first_value, Quote)
        assert isinstance(first_value.time, datetime.datetime)
        assert first_value.price > 0
        assert first_value.volume >= 0

    async def test__get_factsheet(self):
        resp = await self.client.get_factsheet("LU0290358497-ETFP")

        assert resp.isin == "LU0290358497"
        assert resp.code == "NSCIT0IXEON0"
        assert resp.instrument_type == "Trackers"
        assert resp.instrument_sub_type == "ETF"
        assert resp.trading_currency == "EUR"
