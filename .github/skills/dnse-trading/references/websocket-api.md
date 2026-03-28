# DNSE WebSocket API Reference

## TradingClient Constructor

```python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "path/to", "3rdparty", "dnse", "python", "websocket-marketdata"))

from trading_websocket import TradingClient

client = TradingClient(
    api_key=os.environ["DNSE_API_KEY"],
    api_secret=os.environ["DNSE_API_SECRET"],
    base_url="wss://ws-openapi.dnse.com.vn",  # default
    encoding="json",                           # "json" or "msgpack"
    auto_reconnect=True,                       # default
    max_retries=10,                            # default
    heartbeat_interval=25.0,                   # default
    timeout=60.0,                              # default
)
```

Features: auto-reconnect with exponential backoff, HMAC-SHA256 auth, heartbeat monitoring, re-subscribes on reconnect.

---

## Connection Lifecycle

```python
import asyncio

async def main():
    encoding = "msgpack"
    client = TradingClient(
        api_key="key",
        api_secret="secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    await client.connect()              # Connects + authenticates
    # ... subscribe to channels ...
    await asyncio.sleep(8 * 60 * 60)    # Keep alive
    await client.disconnect()           # Graceful shutdown

asyncio.run(main())
```

---

## Subscription Methods

### `subscribe_quotes(symbols, on_quote=None, encoding="json", board_id=None)`
Real-time best bid/ask (BBO) for symbols.

```python
from trading_websocket.models import Quote

def handle_quote(quote: Quote):
    print(f"Best bid: {quote.best_bid}, Best ask: {quote.best_ask}, Spread: {quote.spread}")

await client.subscribe_quotes(["SSI", "HPG"], on_quote=handle_quote, encoding="msgpack", board_id="G1")
```

### `subscribe_trades(symbols, on_trade=None, encoding="json", board_id=None)`
Real-time order matching (tick) data.

```python
from trading_websocket.models import Trade

def handle_trade(trade: Trade):
    print(f"TRADE: {trade.symbol} @ {trade.price} x {trade.quantity}")

await client.subscribe_trades(["SSI"], on_trade=handle_trade, encoding="msgpack", board_id="G1")
```

### `subscribe_trade_extra(symbols, on_trade_extra=None, encoding="json", board_id=None)`
Ticks with additional compiled data (active buy/sell, avg price).

```python
from trading_websocket.models import TradeExtra

def handle(te: TradeExtra):
    print(f"TRADE EXTRA: {te.symbol} side={te.side} avg={te.avgPrice}")

await client.subscribe_trade_extra(["SSI"], on_trade_extra=handle, encoding="msgpack", board_id="G1")
```

### `subscribe_ohlc(symbols, resolution="1", on_ohlc=None, encoding="json")`
Real-time OHLC candle data. No `board_id` parameter.

Resolutions: `"1"`, `"3"`, `"5"`, `"15"`, `"30"`, `"1H"`, `"1D"`, `"1W"`

```python
from trading_websocket.models import Ohlc

def handle_ohlc(ohlc: Ohlc):
    print(f"OHLC: {ohlc.symbol} O={ohlc.open} H={ohlc.high} L={ohlc.low} C={ohlc.close} V={ohlc.volume}")

await client.subscribe_ohlc(["SSI", "VN30F1M", "VN30"], resolution="1", on_ohlc=handle_ohlc, encoding="msgpack")
```

### `subscribe_expected_price(symbols, on_expected_price=None, encoding="json", board_id=None)`
Expected prices during ATO/ATC sessions.

```python
from trading_websocket.models import ExpectedPrice

def handle(ep: ExpectedPrice):
    print(f"Expected: {ep.symbol} price={ep.expectedTradePrice} qty={ep.expectedTradeQuantity}")

await client.subscribe_expected_price(["SSI"], on_expected_price=handle, encoding="msgpack", board_id="G1")
```

### `subscribe_sec_def(symbols, on_sec_def=None, encoding="json", board_id=None)`
Security definition updates (price limits, status changes).

```python
from trading_websocket.models import SecurityDefinition

def handle(sd: SecurityDefinition):
    print(f"SecDef: {sd.symbol} basic={sd.basicPrice} ceil={sd.ceilingPrice} floor={sd.floorPrice}")

await client.subscribe_sec_def(["SSI"], on_sec_def=handle, encoding="msgpack", board_id="G1")
```

### `subscribe_market_index(market_index, on_market_index=None, encoding="json")`
Market index data. No `board_id` parameter.

```python
from trading_websocket.models import MarketIndex

def handle(mi: MarketIndex):
    print(f"Index: {mi.index_name} value={mi.value_indexes} change={mi.changed_ratio}%")

await client.subscribe_market_index(market_index="HNX", on_market_index=handle, encoding="msgpack")
```

### `unsubscribe(channel, symbols)`
Unsubscribe from a channel.

```python
await client.unsubscribe("top_price.G1.msgpack", ["SSI"])
```

---

## Event System

Register custom event handlers with `client.on(event, handler)`:

```python
client.on("trade", lambda t: print(t))
client.on("error", lambda e: print(f"Error: {e}"))
client.on("reconnecting", lambda info: print(f"Reconnecting attempt {info['attempt']}"))
client.on("reconnected", lambda info: print(f"Reconnected: {info['session_id']}"))
```

Events: `trade`, `trade_extra`, `quote`, `ohlc`, `expected_price`, `security_definition`, `market_index`, `order`, `position`, `account`, `error`, `reconnecting`, `reconnected`

---

## Data Models

All models in `trading_websocket.models` have `from_dict(data)` class methods.

### Trade
| Field               | Type  | Description            |
| ------------------- | ----- | ---------------------- |
| `symbol`            | str   | Ticker symbol          |
| `price`             | float | Match price            |
| `quantity`          | int   | Match quantity         |
| `totalVolumeTraded` | int   | Cumulative volume      |
| `grossTradeAmount`  | float | Cumulative trade value |
| `highestPrice`      | float | Session high           |
| `lowestPrice`       | float | Session low            |
| `openPrice`         | float | Session open           |
| `tradingSessionId`  | int   | Session identifier     |

### Quote
| Field            | Type             | Description                  |
| ---------------- | ---------------- | ---------------------------- |
| `symbol`         | str              | Ticker symbol                |
| `bid`            | List[PriceLevel] | Bid levels (price, quantity) |
| `offer`          | List[PriceLevel] | Ask levels (price, quantity) |
| `totalBidQtty`   | float            | Total bid quantity           |
| `totalOfferQtty` | float            | Total offer quantity         |

Properties: `.best_bid -> (price, qty)`, `.best_ask -> (price, qty)`, `.spread -> float`

### Ohlc
| Field                 | Type    | Description    |
| --------------------- | ------- | -------------- |
| `symbol`              | str     | Ticker symbol  |
| `resolution`          | int     | Bar resolution |
| `open/high/low/close` | Decimal | OHLC prices    |
| `volume`              | int     | Bar volume     |
| `time`                | int     | Bar timestamp  |
| `type`                | str     | Bar type       |

### SecurityDefinition
| Field            | Type  | Description     |
| ---------------- | ----- | --------------- |
| `symbol`         | str   | Ticker symbol   |
| `basicPrice`     | float | Reference price |
| `ceilingPrice`   | float | Upper limit     |
| `floorPrice`     | float | Lower limit     |
| `securityStatus` | int   | Trading status  |

### MarketIndex
| Field                 | Type  | Description            |
| --------------------- | ----- | ---------------------- |
| `index_name`          | str   | Index name (e.g., HNX) |
| `value_indexes`       | float | Current value          |
| `changed_ratio`       | float | Change percentage      |
| `changed_value`       | float | Change value           |
| `total_volume_traded` | int   | Total volume           |

### ExpectedPrice
| Field                   | Type  | Description             |
| ----------------------- | ----- | ----------------------- |
| `symbol`                | str   | Ticker symbol           |
| `expectedTradePrice`    | float | Expected match price    |
| `expectedTradeQuantity` | int   | Expected match quantity |

---

## Channel Name Format

WebSocket channels follow the pattern: `{type}.{board_or_param}.{encoding}`

| Subscription   | Channel Pattern                                  |
| -------------- | ------------------------------------------------ |
| Quotes         | `top_price.{board_id}.{json\|msgpack}`           |
| Trades         | `tick.{board_id}.{json\|msgpack}`                |
| Trade Extra    | `tick_extra.{board_id}.{json\|msgpack}`          |
| Expected Price | `expected_price.{board_id}.{json\|msgpack}`      |
| Security Def   | `security_definition.{board_id}.{json\|msgpack}` |
| OHLC           | `ohlc.{resolution}.{json\|msgpack}`              |
| Market Index   | `market_index.{index_name}.{json\|msgpack}`      |
