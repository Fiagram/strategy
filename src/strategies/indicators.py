from abc import ABC, abstractmethod
import talib

class IndicatorAbstract(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

class BollingerBands(IndicatorAbstract):
    def __init__(
            self,
            length: int = 20, 
            std_dev: int = 2,
        ):
        self._length = length
        self._std_dev = std_dev

    def calculate(self, serial: list[float]) -> None:
        self.upper_band, self.middle_band, self.lower_band = talib.BBANDS(
            serial,
            timeperiod=self._length,
            nbdevup=self._std_dev,
            nbdevdn=self._std_dev,
        )
    
    @classmethod
    def from_dict(cls, data: dict) -> "BollingerBands":
        return cls(
            length=data.get("length", 20),
            std_dev=data.get("std_dev", 2),
        )

    def __str__(self) -> str:
        return f"bollinger bands ({self._length}, {self._std_dev})"
    
class RSI(IndicatorAbstract):
    def __init__(
            self,
            length: int = 14,
        ):
        self._length = length

    def calculate(self, serial: list[float]) -> None:
        self.rsi = talib.RSI(serial, timeperiod=self._length)

    @classmethod
    def from_dict(cls, data: dict) -> "RSI":
        return cls(
            length=data.get("length", 14),
        )

    def __str__(self) -> str:
        return f"RSI ({self._length})"

class SMA(IndicatorAbstract):
    def __init__(
            self,
            length: int = 200,
        ):
        self._length = length

    def calculate(self, serial: list[float]) -> None:
        self.moving_average = talib.SMA(serial, timeperiod=self._length)

    @classmethod
    def from_dict(cls, data: dict) -> "SMA":
        return cls(
            length=data.get("length", 200),
        )

    def __str__(self) -> str:
        return f"SMA ({self._length})"
