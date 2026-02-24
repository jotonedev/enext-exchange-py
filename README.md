# enext-exchange-py

Provides access to real-time and historical financial data from various exchanges.

## Features

- **Detailed Quotes**: Get real-time price, change percentages, and last traded time.
- **Intraday Quotes**: Fetch intraday price and volume data.
- **Historical Quotes**: Access historical price and volume data.
- **Factsheets**: Retrieve instrument information such as ISIN, code, instrument type, and trading details.

## Installation

Install the package using pip:

```bash
pip install enext-exchange-py
```

## Quick Start

The library uses `asyncio` for its operations. Below is a simple example of how to use the `ExchangeClient`.

```python
import asyncio
from enext_exchange_py import ExchangeClient

async def main():
    async with ExchangeClient() as client:
        # 1. Get a detailed quote for a ISIN
        symbol = "LU0290358497-ETFP"
        quote = await client.get_detailed_quote(symbol)
        print(f"Name: {quote.name}")

        # 2. Get intraday quotes
        print("\nIntraday Quotes")
        async for q in client.get_intraday_quotes(symbol):
            print(f"{q.time}: {q.price} (Vol: {q.volume})")
            break  # remove to list them all

        # 3. Get a factsheet
        factsheet = await client.get_factsheet(symbol)
        print(f"\nISIN: {factsheet.isin}")
        print(f"Trading Currency: {factsheet.trading_currency}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Usage

### API Methods

- `await get_detailed_quote(symbol: str) -> DetailedQuote`: Returns a `DetailedQuote` object containing the latest market data.
- `get_intraday_quotes(symbol: str) -> AsyncGenerator[Quote, None]`: An async generator yielding `Quote` objects for the current trading day.
- `get_historical_quotes(symbol: str) -> AsyncGenerator[Quote, None]`: An async generator yielding historical `Quote` objects.
- `await get_factsheet(symbol: str) -> Factsheet`: Returns a `Factsheet` object with instrument metadata.
## Development

To set up the development environment, you can use `uv`:

```bash
# Install dependencies
uv sync --all-extras --group dev

# Run tests
uv run pytest
```

## License

This project is licensed under the MIT License.

All data retrieved through this project remains the exclusive property of the respective data providers. Use of this software does not grant any ownership rights or licenses to the underlying data; users are responsible for complying with the providers' specific Terms of Service.
