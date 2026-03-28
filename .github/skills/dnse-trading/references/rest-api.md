# DNSE REST API Reference

## DNSEClient Constructor

```python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "path/to", "3rdparty", "dnse", "python"))

from dnse import DNSEClient

client = DNSEClient(
    api_key=os.environ["DNSE_API_KEY"],
    api_secret=os.environ["DNSE_API_SECRET"],
    base_url="https://openapi.dnse.com.vn",  # default
    algorithm="hmac-sha256",                  # default
    hmac_nonce_enabled=True,                   # default
)
```

All methods return `(status: int, body: str)` or `(None, None)` when `dry_run=True`.

---

## Account & Balance

### `get_accounts(dry_run=False)`
Retrieve all trading sub-accounts.

```python
status, body = client.get_accounts()
```

### `get_balances(account_no, dry_run=False)`
Retrieve asset balances for a sub-account.

```python
status, body = client.get_balances(account_no="0001000115")
```

---

## Positions

### `get_positions(account_no, market_type, dry_run=False)`
Retrieve holding positions.

```python
status, body = client.get_positions(
    account_no="0001000115",
    market_type="DERIVATIVE",  # or "STOCK"
)
```

### `get_position_by_id(market_type, position_id, dry_run=False)`
Retrieve a specific position by ID.

```python
status, body = client.get_position_by_id(
    position_id="some-position-id",
    market_type="STOCK",
)
```

---

## Orders

### `get_orders(account_no, market_type, order_category=None, dry_run=False)`
Retrieve intraday order book.

```python
status, body = client.get_orders(
    account_no="0001000115",
    market_type="STOCK",
    order_category="NORMAL",  # optional
)
```

### `get_order_detail(account_no, order_id, market_type, order_category=None, dry_run=False)`
Retrieve details for a specific order.

```python
status, body = client.get_order_detail(
    account_no="0001000115",
    order_id="801",
    market_type="STOCK",
    order_category="NORMAL",
)
```

### `get_order_history(account_no, market_type, from_date=None, to_date=None, page_size=None, page_index=None, dry_run=False)`
Retrieve historical orders with pagination.

```python
status, body = client.get_order_history(
    account_no="0001000115",
    market_type="STOCK",
    from_date="2025-12-01",
    to_date="2025-12-09",
    page_size=20,
    page_index=1,
)
```

---

## Trading Operations

All trading operations require a `trading_token` obtained via the OTP flow.

### OTP Flow

```python
# Step 1: Request OTP email
status, body = client.send_email_otp()

# Step 2: Exchange OTP for trading token
status, body = client.create_trading_token(
    otp_type="email_otp",
    passcode="666666",  # OTP from email
)
# Parse trading_token from body
```

### `post_order(market_type, payload, trading_token, order_category="NORMAL", dry_run=False)`
Place a new order.

```python
payload = {
    "accountNo": "0001000115",
    "symbol": "HPG",
    "side": "BUY",
    "orderType": "LO",
    "price": 25950,
    "quantity": 100,
    "loanPackageId": 2396,
}

status, body = client.post_order(
    market_type="STOCK",
    payload=payload,
    trading_token="your-trading-token",
    order_category="NORMAL",
)
```

### `put_order(account_no, order_id, market_type, payload, trading_token, order_category=None, dry_run=False)`
Modify an existing order.

```python
payload = {
    "price": 12500,
    "quantity": 100,
}

status, body = client.put_order(
    account_no="0001000115",
    order_id="511",
    market_type="STOCK",
    payload=payload,
    trading_token="your-trading-token",
    order_category="NORMAL",
)
```

### `cancel_order(account_no, order_id, market_type, trading_token, order_category=None, dry_run=False)`
Cancel an existing order.

```python
status, body = client.cancel_order(
    account_no="0001000115",
    order_id="801",
    market_type="STOCK",
    trading_token="your-trading-token",
    order_category="NORMAL",
)
```

### `close_position(position_id, market_type, payload, trading_token, dry_run=False)`
Close a position (typically for derivatives).

```python
status, body = client.close_position(
    position_id="some-position-id",
    market_type="DERIVATIVE",
    payload={},
    trading_token="your-trading-token",
)
```

---

## Market Data

### `get_ppse(account_no, market_type, symbol, price, loan_package_id, dry_run=False)`
Check buying/selling power before placing an order.

```python
status, body = client.get_ppse(
    account_no="0001000115",
    market_type="STOCK",
    symbol="HPG",
    price=26450,
    loan_package_id=2396,
)
```

### `get_loan_packages(account_no, market_type, symbol=None, dry_run=False)`
Retrieve available loan package codes (required for order placement).

```python
status, body = client.get_loan_packages(
    account_no="0001000115",
    market_type="STOCK",
    symbol="SCR",  # optional
)
```

### `get_security_definition(symbol, board_id=None, dry_run=False)`
Get security definition (reference prices, status).

```python
status, body = client.get_security_definition(symbol="HPG")
```

### `get_ohlc(bar_type, query=None, dry_run=False)`
Get OHLC candlestick data.

```python
status, body = client.get_ohlc(
    bar_type="STOCK",
    query={
        "symbol": "HPG",
        "resolution": "1",       # "1","3","5","15","30","1H","1D","1W"
        "from": 1735689600,      # Unix timestamp
        "to": 1735776000,
    },
)
```

### `get_trades(symbol, board_id=None, from_date=None, to_date=None, limit=None, order=None, next_page_token=None, dry_run=False)`
Get historical trade ticks.

```python
status, body = client.get_trades(
    symbol="GAS",
    board_id="G1",
    from_date=1773282637,
    to_date=1773289837,
    limit=100,
    order="DESC",
)
```

### `get_instruments(symbol=None, market_id=None, security_group_id=None, index_name=None, limit=None, page=None, dry_run=False)`
Search/list instruments.

```python
status, body = client.get_instruments(
    symbol="SSI,SHS,ACB",
    limit=100,
    page=1,
)
```

### `get_latest_trade(symbol, board_id=None, dry_run=False)`
Get the most recent trade for a symbol.

```python
status, body = client.get_latest_trade(symbol="GAS", board_id="G1")
```
