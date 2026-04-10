from abc import ABC, abstractmethod

class CompareAbstract(ABC):
    @abstractmethod
    def check (self, compare : float) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class UnaryCompareAbstract(CompareAbstract):
    def __init__(self , value: float):
        self._value = value

class SerialCompareAbstract(CompareAbstract):
    def __init__(self , serial: list[float]):
        if len(serial) < 2:
            raise ValueError("input must have at least 2 elements")
        self._serial = serial

class GreaterThan(UnaryCompareAbstract):
    def check(self, number: float) -> bool:
        return self._value > number

    def __str__(self) -> str:
        return "greater than"
    
class LessThan(UnaryCompareAbstract):
    def check(self, number: float) -> bool:
        return self._value < number

    def __str__(self) -> str:
        return "less than"

class CrossingUp(SerialCompareAbstract):
    def check(self, number: float) -> bool:
        return self._serial[1] < number and self._serial[0] > number

    def __str__(self) -> str:
        return "crossing up"

class CrossingDown(SerialCompareAbstract):
    def check(self, number: float) -> bool:
        return self._serial[1] > number and self._serial[0] < number

    def __str__(self) -> str:
        return "crossing down"

class MovingUp(SerialCompareAbstract):
    def __init__(self, serial: list[float], percentage: float = 1.0):
        super().__init__(serial)
        self._percentage = percentage

    def check(self, number: float) -> bool:
        return self._serial[1] < number and self._serial[0] > number * (1 + self._percentage / 100)

    def __str__(self) -> str:
        return f"moving up by {self._percentage}%"

class MovingDown(SerialCompareAbstract):
    def __init__(self, serial: list[float], percentage: float = 1.0):
        super().__init__(serial)
        self._percentage = percentage

    def check(self, number: float) -> bool:
        return self._serial[1] > number and self._serial[0] < number * (1 - self._percentage / 100)

    def __str__(self) -> str:
        return f"moving down by {self._percentage}%"