import base64
import hashlib
import json
from typing import Final

import httpx
from httpx import URL
from Crypto.Cipher import AES

from enext_exchange_py.models import EncryptedResponse
from enext_exchange_py.models.enums import DownloadFormat, DateFormat, DecimalSeparator

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
        secret: str | bytes = DEFAULT_SECRET,\
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
    def _obtain_key(password: bytes, salt: bytes, key_len: int, iv_len: int):
        """
        Derives key and IV from password and salt
        """
        dtot = b""
        d = b""
        while len(dtot) < (key_len + iv_len):
            # Hash current digest + password + salt
            d = hashlib.md5(d + password + salt).digest()
            dtot += d
        return dtot[:key_len], dtot[key_len:key_len + iv_len]

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

    def get_detailed_quote(self, symbol: str):
        path = f"/{self._language}/ajax/getDetailedQuote/{symbol}"
        raise NotImplementedError

    def get_intraday_quotes(self, symbol: str):
        path = f"/intraday_chart/getChartData/{symbol}/intraday"
        raise NotImplementedError

    def get_historical_quotes(self, symbol: str):
        path = f"/intraday_chart/getChartData/{symbol}/max"
        raise NotImplementedError

    def get_performance_book(self, symbol: str):
        path = f"/{self._language}/ajax/getPerformancesBook/{symbol}"
        raise NotImplementedError

    def get_factsheets(self, symbol: str):
        path = f"/{self._language}/ajax/getDetailedQuoteFactsheets/{symbol}"
        raise NotImplementedError
