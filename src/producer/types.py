from abc import ABC, abstractmethod

class ProducerSignalAbstract(ABC):
    def __init__(
            self,
            timestamp: int,
            ): 
        self._timestamp = timestamp

    @abstractmethod
    def topic (self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class TorchSignal(ProducerSignalAbstract):
    def __init__(
            self,
            symbol: str,
            indicator: str,
            operator: str,
            timestamp: int,
            ):
        super().__init__(timestamp)
        self._symbol = symbol
        self._indicator = indicator
        self._operator = operator

    def topic(self) -> str:
        return "torch"

    def __str__(self) -> str:
        return f"TorchSignal(message={self._message}, timestamp={self._timestamp})"
