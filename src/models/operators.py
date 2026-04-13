from abc import ABC, abstractmethod

class CompareAbstract(ABC):
    def __init__(self , refer_value: float = 0.0):
        self._refer_value = refer_value

    @abstractmethod
    def set_refer_value(self, refer_value: float) -> None:
        self._refer_value = refer_value

    @abstractmethod
    def check (self, compare : float) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class GreaterThan(CompareAbstract):
    def check(self, value: float) -> bool:
        return self._refer_value > value

    def __str__(self) -> str:
        return "greater than"
    
class LessThan(CompareAbstract):
    def check(self, value: float) -> bool:
        return self._refer_value < value

    def __str__(self) -> str:
        return "less than"

class CrossingUp(CompareAbstract):
    def __init__(self, refer_value: float):
        super().__init__(refer_value)
        self._isPrevStateCorrect = False

    def check(self, value: float) -> bool:
        if not self._isPrevStateCorrect and value < self._refer_value:
            self._isPrevStateCorrect = True
        elif self._isPrevStateCorrect and value > self._refer_value:
            self._isPrevStateCorrect = False
            return True
        return False
        
    def __str__(self) -> str:
        return "crossing up"

class CrossingDown(CompareAbstract):
    def __init__(self, refer_value: float):
        super().__init__(refer_value)
        self._isPrevStateCorrect = False

    def check(self, value: float) -> bool:
        if not self._isPrevStateCorrect and value > self._refer_value:
            self._isPrevStateCorrect = True
        elif self._isPrevStateCorrect and value < self._refer_value:
            self._isPrevStateCorrect = False
            return True
        return False

    def __str__(self) -> str:
        return "crossing down"

class MovingUp(CompareAbstract):
    def __init__(self, refer_value: float, percentage: float = 1.0):
        super().__init__(refer_value)
        self._isPrevStateCorrect = False
        self._percentage = percentage

    def check(self, value: float) -> bool:
        if not self._isPrevStateCorrect and value < self._refer_value:
            self._isPrevStateCorrect = True
        elif self._isPrevStateCorrect and value > self._refer_value * (1 + self._percentage / 100):
            self._isPrevStateCorrect = False
            return True
        return False
            
    def __str__(self) -> str:
        return f"moving up {self._percentage}%"

class MovingDown(CompareAbstract):
    def __init__(self, refer_value: float, percentage: float = 1.0):
        super().__init__(refer_value)
        self._isPrevStateCorrect = False
        self._percentage = percentage

    def check(self, value: float) -> bool:
        if not self._isPrevStateCorrect and value > self._refer_value:
            self._isPrevStateCorrect = True
        elif self._isPrevStateCorrect and value < self._refer_value * (1 - self._percentage / 100):
            self._isPrevStateCorrect = False
            return True
        return False

    def __str__(self) -> str:
        return f"moving down {self._percentage}%"