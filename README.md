# enext-exchange-py

Provides access to real-time and historical financial data from various exchanges.

## Features

- **Detailed Quotes**: Get real-time price, change percentages, and last traded time.
- **Intraday Quotes**: Fetch intraday price and volume data.
- **Historical Quotes**: Access historical price and volume data.
- **Factsheets**: Retrieve instrument information such as ISIN, code, instrument type, and trading details.
- **Asynchronous**: Built on `httpx`

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
        # 1. Get a detailed quote for a symbol (e.g., Lyxor MSCI World ETF)
        symbol = "LU0290358497-ETFP"
        quote = await client.get_detailed_quote(symbol)
        print(f"Name: {quote.name}")
        print(f"Last Price: {quote.last_traded_price.value} {quote.last_traded_price.currency}")
        print(f"Change: {quote.since_previous_close_percentage}%")

        # 2. Get intraday quotes
        print("\nIntraday Quotes (first 5):")
        async for q in client.get_intraday_quotes(symbol):
            print(f"{q.time}: {q.price} (Vol: {q.volume})")
            # Limit for demonstration
            break 

        # 3. Get a factsheet
        factsheet = await client.get_factsheet(symbol)
        print(f"\nISIN: {factsheet.isin}")
        print(f"Instrument Type: {factsheet.instrument_type}")
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

This project is licensed under the terms of the license included in the repository.
