from dataclasses import dataclass


@dataclass
class TPSL:
    volume: float
    price: float
    percentage: float


@dataclass
class TakeProfit(TPSL):
    pass


@dataclass
class StopLoss(TPSL):
    pass


@dataclass
class TakeProfitFibPer:
    fib_mark: float
    vol_per: float

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.fib_mark}, {self.vol_per})"
