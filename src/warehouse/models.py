from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Dict

class Timeframe(StrEnum):
    DAY_1 = "1D"
    WEEK_1 = "1W"
    MONTH_1 = "1M"

@dataclass
class Ohlcv:
    open: float
    high: float
    low: float
    close: float
    volume: int

    @classmethod
    def from_dnse_client_json(cls, data: Dict[str, Any]) -> "Ohlcv":
        return cls(
            open=data.get("o"),
            high=data.get("h"),
            low=data.get("l"),
            close=data.get("c"),
            volume=data.get("v")
        )
    
    @classmethod
    def from_dnse_websocket_json(cls, data: Dict[str, Any]) -> "Ohlcv":
        return cls(
            open=data.get("open"),
            high=data.get("high"),
            low=data.get("low"),
            close=data.get("close"),
            volume=data.get("volume")
        )

Symbol = str

