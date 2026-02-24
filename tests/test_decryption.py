import httpx

from enext_exchange_py.client import DEFAULT_SECRET, ExchangeClient
from enext_exchange_py.models import EncryptedResponse


def test__decrypt_data():
    url = "https://live.euronext.com/en/intraday_chart/getChartData/IE00BP3QZB59-ETFP/intraday"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    with httpx.Client(follow_redirects=True) as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    er = EncryptedResponse(ct=data["ct"], s=data["s"], iv=data["iv"])

    # Decrypt data
    decrypted = ExchangeClient._decrypt_data(er, DEFAULT_SECRET.encode())

    # Assertions
    assert isinstance(decrypted, list)
    assert len(decrypted) > 0
    # Check if first element has expected keys for intraday data
    first_point = decrypted[0]
    assert "time" in first_point
    assert "price" in first_point
