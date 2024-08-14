from dataclasses import dataclass

from tradex.constants.enuming import Direction


@dataclass
class OrderProfitFormSimple:
    price: float
    size: float

    # fib mark to calculate fibonacci retracement
    zero_mark: float
    middle_mark: float

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must grater than 0")

    @property
    def order_type(self) -> Direction:
        return Direction.LONG if self.middle_mark > self.zero_mark else Direction.SHORT

    @property
    def order_price(self) -> float:
        return self.price * self.size
