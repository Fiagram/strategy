from abc import ABC, abstractmethod
import talib

class IndicatorAbstract(ABC):
    @abstractmethod
    def refresh(self, serial: list[float]) -> None:
        pass

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

    def refresh(self, serial: list[float]) -> None:
        self.upper_band, self.middle_band, self.lower_band = talib.BBANDS(
            serial,
            timeperiod=self._length,
            nbdevup=self._std_dev,
            nbdevdn=self._std_dev,
        )

    def __str__(self) -> str:
        return f"bollinger bands ({self._length}, {self._std_dev})"
    
class RSI(IndicatorAbstract):
    def __init__(
            self,
            length: int = 14,
        ):
        self._length = length

    def refresh(self, serial: list[float]) -> None:
        self.rsi = talib.RSI(serial, timeperiod=self._length)
    
    def __str__(self) -> str:
        return f"RSI ({self._length})"
    

class SMA(IndicatorAbstract):
    def __init__(
            self,
            length: int,
        ):
        self._length = length

    def refresh(self, serial: list[float]) -> None:
        self.sma = talib.SMA(serial, timeperiod=self._length)
    
    def __str__(self) -> str:
        return f"SMA ({self._length})"
    
class SMA10(SMA):
    def __init__(self):
        super().__init__(length=10)

class SMA50(SMA):
    def __init__(self):
        super().__init__(length=50)

class SMA100(SMA):
    def __init__(self):
        super().__init__(length=100)

class SMA200(SMA):
    def __init__(self):
        super().__init__(length=200)
