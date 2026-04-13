from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, UTC
from handlers.producer.models import TorchSignal
from .operators import CompareAbstract

Symbol = str
class IndicatorName(Enum):
    CLOSE = "CLOSE"
    BOLLINGER_BANDS = "BOLLINGER_BANDS"
    RSI = "RSI"
    SMA10 = "SMA10"
    SMA20 = "SMA20"
    SMA50 = "SMA50"
    SMA100 = "SMA100"
    SMA200 = "SMA200"

class Timeframe(Enum):
    DAY_1 = "1D"
    WEEK_1 = "1W"
    MONTH_1 = "1M"

class Trigger(Enum):
    ONLY_ONE = "ONCE"
    EVERYTIME = "EVERY"

class OhlcvLabel(Enum):
    OPEN = "open price"
    HIGH = "high price"
    LOW = "low price"
    CLOSE = "close price"
    VOLUME = "volume"

class Ohlcv:
    def __init__(self, label: OhlcvLabel, value: float = 0.0):
        self.label = str(label.value)
        self.value = value

class ReferByGivenValue:
    def __init__(self, label: str, value: float):
        self.label = label
        self.value = value

class AlertByOhlcv:
    def __init__(
            self,
            of_account_id: int, 
            timeframe: Timeframe,
            symbol: str,
            ohlcv: Ohlcv,
            refer: ReferByGivenValue,
            operator: CompareAbstract,
            trigger: Trigger,
            exp: int,
            message: str | None = None,
        ): 
        self._of_account_id = of_account_id
        self._timeframe = timeframe
        self._symbol = symbol
        self._ohlcv = ohlcv
        self._refer = refer
        self._operator = operator
        self._operator.set_refer_value(refer.value)
        self._trigger = trigger
        self._exp = exp
        self._message = message

    def check(self, value: float) -> bool:
        if self._operator.check(value):
            self._ohlcv.value = value
            return True

    def to_torch_signal(self) -> TorchSignal:
        if self._exp < int(datetime.now(UTC).timestamp()):
            raise ValueError("Alert has expired")
        if self._message is None:
            self._message = f"[{self._symbol}] [{self._timeframe.value}] The {self._ohlcv.label} ({self._ohlcv.value}) is {self._operator} {self._refer.label} ({self._refer.value})"
        return TorchSignal(of_account_id=self._of_account_id, message=self._message)

    # TODO: Complete this method
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            of_account_id=data["of_account_id"],
            timeframe=Timeframe(data["timeframe"]),
            symbol=data["symbol"],
            ohlcv=Ohlcv(label=OhlcvLabel(data["ohlcv"]["label"]), value=data["ohlcv"]["value"]),
            refer=ReferByGivenValue(label=data["refer"]["label"], value=data["refer"]["value"]),
            operator=CompareAbstract.from_dict(data["operator"]),
            trigger=Trigger(data["trigger"]),
            exp=data["exp"],
            message=data.get("message")
        )