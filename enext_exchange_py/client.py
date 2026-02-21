import base64
import datetime
import hashlib
import json
from parsel import Selector
from typing import Final, Any, Generator, AsyncGenerator, Coroutine

import httpx
from httpx import URL
from Crypto.Cipher import AES

from enext_exchange_py.models import EncryptedResponse, DetailedQuote, Quote
from enext_exchange_py.mappers import map_page_to_detailed_quote, map_page_to_factsheet

__all__ = ["ExchangeClient"]

DEFAULT_BASE_URL: Final[str] = "https://live.euronext.com"
DEFAULT_HEADERS: Final[dict] = {
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
}
DEFAULT_SECRET: Final[str] = "24ayqVo7yJma"


class ExchangeClient:
    _client: httpx.AsyncClient

    def __init__(
        self,
        base_url: URL | str = DEFAULT_BASE_URL,
        headers: dict | None = None,
        secret: str | bytes = DEFAULT_SECRET,
        language: str = "en",
        *args,
        **kwargs,
    ):
        if isinstance(base_url, str):
            base_url = URL(base_url)
        self.base_url = base_url

        if headers is None:
            self.headers = DEFAULT_HEADERS

        self._cookies = httpx.Cookies()
        self._client = httpx.AsyncClient(
            cookies=self._cookies,
            headers=headers,
            base_url=self.base_url,
            follow_redirects=True,
            *args,
            **kwargs,
        )
        if isinstance(secret, str):
            self._secret = secret.encode()
        self._language = language

    @staticmethod
    def _obtain_key(password: bytes, salt: bytes, key_len: int, iv_len: int) -> tuple[bytes, bytes]:
        """
        Derives key and IV from password and salt. Uses PBKDF2 with md5 as a hash function.
        """
        dtot = b""
        d = b""
        while len(dtot) < (key_len + iv_len):
            # Hash current digest + password + salt
            d = hashlib.md5(d + password + salt).digest()
            dtot += d
        return dtot[:key_len], dtot[key_len : key_len + iv_len]

    @staticmethod
    def _decrypt_data(resp: EncryptedResponse, secret: bytes) -> dict | list:
        salt = bytes.fromhex(resp.s)
        ct = base64.b64decode(resp.ct)

        key, iv = ExchangeClient._obtain_key(secret, salt, 32, 16)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_bytes = cipher.decrypt(ct)
        # PKCS7 unpadding
        padding_len = decrypted_bytes[-1]
        if padding_len < 1 or padding_len > 16:
            # Fallback or error if padding is not valid PKCS7
            decrypted = decrypted_bytes.decode("utf-8")
        else:
            decrypted = decrypted_bytes[:-padding_len].decode("utf-8")

        return json.loads(decrypted)

    async def get_detailed_quote(self, symbol: str) -> DetailedQuote:
        path = f"/{self._language}/ajax/getDetailedQuote/{symbol}"

        resp = await self._client.get(path)
        page = Selector(resp.text)

        data = map_page_to_detailed_quote(page)
        return data

    @staticmethod
    def _parse_quotes_list(quotes_list: list[dict[str, Any]]) -> Generator[Quote, None, None]:
        for item in quotes_list:
            date_str = item.pop("time")
            item["time"] = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            yield Quote(**item)

    async def get_intraday_quotes(self, symbol: str) -> Generator[Quote, None, None]:
        path = f"/intraday_chart/getChartData/{symbol}/intraday"

        resp = await self._client.get(path)
        enc_data = EncryptedResponse(**resp.json())
        data = self._decrypt_data(enc_data, self._secret)

        return self._parse_quotes_list(data)

    async def get_historical_quotes(self, symbol: str) -> Generator[Quote, None]:
        path = f"/intraday_chart/getChartData/{symbol}/max"

        resp = await self._client.get(path)
        enc_data = EncryptedResponse(**resp.json())
        data = self._decrypt_data(enc_data, self._secret)

        return self._parse_quotes_list(data)

    async def get_factsheet(self, symbol: str):
        path = f"/{self._language}/ajax/getDetailedQuoteFactsheets/{symbol}"

        resp = await self._client.get(path)
        page = Selector(resp.text)

        data = map_page_to_factsheet(page)
        return data
