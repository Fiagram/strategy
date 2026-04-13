from abc import ABC, abstractmethod

class ProducerSignalAbstract(ABC):
    @abstractmethod
    def topic (self) -> str:
        pass

    @abstractmethod
    def payload (self) -> str:
        pass

class TorchSignal(ProducerSignalAbstract):
    def __init__(
            self,
            of_account_id: int,
            message: str,
            ):
        self._of_account_id = of_account_id
        self._message = message

    def topic(self) -> str:
        return "torch"
    
    def payload(self) -> str:
        return self._message
