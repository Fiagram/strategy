from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, UTC

from strategies.operators import CompareAbstract

class Timeframe(Enum):
    DAY_1 = "1D"
    WEEK_1 = "1W"
    MONTH_1 = "1M"

class Trigger(Enum):
    ONLY_ONE = "ONLY_ONE"
    EVERYTIME = "EVERYTIME"


class StrategyAbstract(ABC):
    def __init__(
            self,
            symbols: list[str],
            timeframe: Timeframe,
            operator: CompareAbstract,
            trigger: Trigger,
            issue_at: datetime,
            expire_at: datetime,
        ): 
        pass

    @abstractmethod 
    def __str__(self) -> str:
        pass