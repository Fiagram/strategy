---
name: dnse-trading
description: "Use the DNSE Python trading library for REST API and WebSocket market data. USE FOR: placing orders, querying accounts/balances/positions/orders, getting OHLC/trades/quotes, subscribing to real-time WebSocket market data, building trading strategies with DNSE OpenAPI."
argument-hint: "Describe the trading operation or market data task you want to implement"
---

# DNSE Trading Library

Use the DNSE Python SDK located at `3rdparty/dnse/python/` for all trading and market data operations.

## When to Use

- Interact with DNSE OpenAPI (accounts, orders, positions, balances)
- Place, modify, or cancel trading orders
- Retrieve market data (OHLC, trades, quotes, security definitions)
- Subscribe to real-time WebSocket market data streams
- Build automated trading strategies

## Library Structure

```
3rdparty/dnse/python/
├── dnse/                    # REST API client
│   ├── __init__.py          # Exports DNSEClient
│   ├── client.py            # DNSEClient class
│   └── common.py            # HMAC signature utilities
├── trading-api/             # REST API examples
└── websocket-marketdata/    # WebSocket examples
    └── trading_websocket/   # WebSocket client package
        ├── client.py        # TradingClient class
        ├── models.py        # Data models (Trade, Quote, Ohlc, etc.)
        ├── connection.py    # WebSocket connection manager
        ├── auth.py          # HMAC-SHA256 auth
        ├── encoding.py      # JSON/MessagePack encoding
        └── exceptions.py    # Error types
```

## Setup

### Credentials

Always load credentials from environment variables — never hardcode them:

```python
import os

api_key = os.environ["DNSE_API_KEY"]
api_secret = os.environ["DNSE_API_SECRET"]
```

### Import Path

The library is vendored inline. Add the path before importing:

```python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "path/to", "3rdparty", "dnse", "python"))
```

For WebSocket imports, also add the `websocket-marketdata` subdirectory:

```python
sys.path.append(os.path.join(os.path.dirname(__file__), "path/to", "3rdparty", "dnse", "python", "websocket-marketdata"))
```

Adjust `"path/to"` based on the script's location relative to the project root.

## REST API — DNSEClient

### Initialization

```python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "path/to", "3rdparty", "dnse", "python"))

from dnse import DNSEClient

client = DNSEClient(
    api_key=os.environ["DNSE_API_KEY"],
    api_secret=os.environ["DNSE_API_SECRET"],
    base_url="https://openapi.dnse.com.vn",
)
```

All methods return `(status_code: int, body: str)`. Use `dry_run=True` to preview requests without sending.

### Available Methods

See [REST API Reference](./references/rest-api.md) for full method signatures and examples.

| Category | Methods |
|----------|---------|
| **Account** | `get_accounts()`, `get_balances(account_no)` |
| **Positions** | `get_positions(account_no, market_type)`, `get_position_by_id(market_type, position_id)` |
| **Orders** | `get_orders(account_no, market_type)`, `get_order_detail(account_no, order_id, market_type)`, `get_order_history(account_no, market_type, ...)` |
| **Trading** | `post_order(market_type, payload, trading_token)`, `put_order(account_no, order_id, market_type, payload, trading_token)`, `cancel_order(account_no, order_id, market_type, trading_token)`, `close_position(position_id, market_type, payload, trading_token)` |
| **Auth/OTP** | `send_email_otp()`, `create_trading_token(otp_type, passcode)` |
| **Market Data** | `get_ppse(account_no, market_type, symbol, price, loan_package_id)`, `get_loan_packages(account_no, market_type)`, `get_security_definition(symbol)`, `get_ohlc(bar_type, query)`, `get_trades(symbol, ...)`, `get_instruments(...)`, `get_latest_trade(symbol)` |

### Key Patterns

**market_type values**: `"STOCK"`, `"DERIVATIVE"`

**Order placement flow** (requires trading token):
1. `send_email_otp()` — request OTP
2. `create_trading_token(otp_type="email_otp", passcode="...")` — get token
3. `post_order(market_type, payload, trading_token)` — place order

**Order payload structure**:
```python
payload = {
    "accountNo": "0001000115",
    "symbol": "HPG",
    "side": "BUY",         # "BUY" or "SELL"
    "orderType": "LO",     # "LO", "MP", "ATO", "ATC", etc.
    "price": 25950,
    "quantity": 100,
    "loanPackageId": 2396,
}
```

**OHLC query structure**:
```python
status, body = client.get_ohlc(
    bar_type="STOCK",
    query={
        "symbol": "HPG",
        "resolution": "1",        # "1", "3", "5", "15", "30", "1H", "1D", "1W"
        "from": 1735689600,       # Unix timestamp
        "to": 1735776000,
    },
)
```

## WebSocket — TradingClient

### Initialization

```python
import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "path/to", "3rdparty", "dnse", "python", "websocket-marketdata"))

from trading_websocket import TradingClient

client = TradingClient(
    api_key=os.environ["DNSE_API_KEY"],
    api_secret=os.environ["DNSE_API_SECRET"],
    base_url="wss://ws-openapi.dnse.com.vn",
    encoding="msgpack",  # "json" or "msgpack"
)
```

### Connection Lifecycle

```python
async def main():
    await client.connect()           # Connect + authenticate
    # ... subscribe to channels ...
    await asyncio.sleep(duration)    # Keep alive
    await client.disconnect()        # Graceful shutdown

asyncio.run(main())
```

### Subscription Methods

See [WebSocket Reference](./references/websocket-api.md) for full details and data models.

All subscribe methods accept an `encoding` parameter (`"json"` or `"msgpack"`) and a callback handler.

| Method | Callback Type | Description |
|--------|--------------|-------------|
| `subscribe_quotes(symbols, on_quote, encoding, board_id)` | `Quote` | Best bid/ask prices |
| `subscribe_trades(symbols, on_trade, encoding, board_id)` | `Trade` | Order matching ticks |
| `subscribe_trade_extra(symbols, on_trade_extra, encoding, board_id)` | `TradeExtra` | Ticks + active buy/sell, avg price |
| `subscribe_ohlc(symbols, resolution, on_ohlc, encoding)` | `Ohlc` | OHLC candles |
| `subscribe_expected_price(symbols, on_expected_price, encoding, board_id)` | `ExpectedPrice` | ATO/ATC expected prices |
| `subscribe_sec_def(symbols, on_sec_def, encoding, board_id)` | `SecurityDefinition` | Security definition updates |
| `subscribe_market_index(market_index, on_market_index, encoding)` | `MarketIndex` | Market index data (e.g., `"HNX"`) |

### WebSocket Pattern

```python
from trading_websocket.models import Quote

encoding = "msgpack"
client = TradingClient(
    api_key=os.environ["DNSE_API_KEY"],
    api_secret=os.environ["DNSE_API_SECRET"],
    base_url="wss://ws-openapi.dnse.com.vn",
    encoding=encoding,
)

def handle_quote(quote: Quote):
    print(f"Best bid: {quote.best_bid}, Best ask: {quote.best_ask}, Spread: {quote.spread}")

await client.connect()
await client.subscribe_quotes(["SSI", "HPG"], on_quote=handle_quote, encoding=encoding, board_id="G1")
await asyncio.sleep(3600)
await client.disconnect()
```

### OHLC Resolutions

`"1"`, `"3"`, `"5"`, `"15"`, `"30"`, `"1H"`, `"1D"`, `"1W"`

### board_id Values

When `board_id` is omitted, subscriptions cover all boards: `G1` through `G7`. Specify a single board to filter.

## Data Models

Import from `trading_websocket.models`:

- `Trade` — match price/qty, volume, high/low/open, session ID
- `TradeExtra` — Trade fields + side (buy/sell indicator), avg price
- `Quote` — bid/offer arrays of `PriceLevel(price, quantity)`, with `.best_bid`, `.best_ask`, `.spread` properties
- `Ohlc` — symbol, resolution, open/high/low/close, volume, time
- `ExpectedPrice` — expected trade price/qty during ATO/ATC
- `SecurityDefinition` — basic/ceiling/floor prices, security status
- `MarketIndex` — index value, change ratio, volume, up/down counts

All models have a `from_dict(data)` class method and support both PascalCase (JSON) and snake_case (MessagePack) field names.

## Exceptions

```python
from trading_websocket.exceptions import (
    TradingWebSocketError,    # Base
    ConnectionError,          # Connection failed
    ConnectionClosed,         # Connection dropped (.recoverable flag)
    AuthenticationError,      # Auth failed
    SubscriptionError,        # Subscription failed
    EncodingError,            # Encode/decode failed
)
```

## Important Notes

- REST client uses `urllib3.PoolManager` internally — thread-safe, connection reuse
- WebSocket client has auto-reconnect with exponential backoff (re-auth + re-subscribe)
- Always use `encoding` parameter consistently between `TradingClient` init and subscribe calls
- Trading operations (post/put/cancel order, close position) require a `trading_token` header
- The `get_ppse()` method checks buying/selling power before placing an order
