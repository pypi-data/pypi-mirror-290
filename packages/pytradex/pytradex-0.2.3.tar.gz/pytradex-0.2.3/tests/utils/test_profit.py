import pytest

from tradex.constants.enuming import ProfitPossibility
from tradex.models.order import OrderProfitFormSimple
from tradex.models.take_profit import TakeProfit, TakeProfitFibPer
from tradex.utils.profit import get_take_profit_fib_per_lst, take_profit_list, take_profit_total

cases = [
    # long
    (
        # OrderProfitFormSimple
        OrderProfitFormSimple(0.1, 1000, 0, 1),
        # TakeProfit list
        [
            TakeProfit(volume=150.0, price=1.382, percentage=0.15),
            TakeProfit(volume=300.0, price=1.618, percentage=0.30),
            TakeProfit(volume=400.0, price=2, percentage=0.40),
            TakeProfit(volume=150.0, price=2.618, percentage=0.15),
            TakeProfit(volume=0, price=3, percentage=0),
        ],
        # total profit
        17854.0,
    ),
    # short
    (
        OrderProfitFormSimple(1, 1000, 1, 0),
        [
            TakeProfit(volume=150.0, price=-0.382, percentage=0.15),
            TakeProfit(volume=300.0, price=-0.618, percentage=0.30),
            TakeProfit(volume=400.0, price=-1, percentage=0.40),
            TakeProfit(volume=150.0, price=-1.618, percentage=0.15),
            TakeProfit(volume=0, price=-2, percentage=0),
        ],
        # total profit
        1885.4,
    ),
    # long normal
    (
        OrderProfitFormSimple(1.784, 665, 1.67, 1.89),
        [
            TakeProfit(volume=99.75, price=1.974, percentage=0.15),
            TakeProfit(volume=199.5, price=2.026, percentage=0.3),
            TakeProfit(volume=266.0, price=2.11, percentage=0.4),
            TakeProfit(volume=99.75, price=2.246, percentage=0.15),
            TakeProfit(volume=0, price=2.33, percentage=0),
        ],
        # total profit
        112.13,
    ),
    # short normal
    (
        OrderProfitFormSimple(1.89, 665, 1.931, 1.784),
        [
            TakeProfit(volume=99.75, price=1.728, percentage=0.15),
            TakeProfit(volume=199.5, price=1.693, percentage=0.3),
            TakeProfit(volume=266.0, price=1.637, percentage=0.4),
            TakeProfit(volume=99.75, price=1.546, percentage=0.15),
            TakeProfit(volume=0, price=1.49, percentage=0),
        ],
        # total profit
        83.11,
    ),
    (
        OrderProfitFormSimple(2636.0, 411.88, 2742.0, 2646.0),
        [
            TakeProfit(volume=61.782, price=2609.328, percentage=0.15),
            TakeProfit(volume=123.564, price=2586.672, percentage=0.3),
            TakeProfit(volume=164.752, price=2550.0, percentage=0.4),
            TakeProfit(volume=61.782, price=2490.672, percentage=0.15),
            TakeProfit(volume=0.0, price=2454.0, percentage=0),
        ],
        # total profit
        11.72,
    ),
]


@pytest.mark.parametrize(("order_profit", "take_profits"), [(case[0], case[1]) for case in cases])
def test_take_profit_list(order_profit, take_profits):
    tp_fib = take_profit_list(order=order_profit)
    assert tp_fib == take_profits


@pytest.mark.parametrize(("order_profit", "take_profits", "total_profit"), cases)
def test_take_profit_total(order_profit, take_profits, total_profit):
    total = take_profit_total(order=order_profit, take_profits=take_profits)
    assert total == total_profit


@pytest.mark.parametrize(
    ("tpp", "expect"),
    [
        (
            ProfitPossibility.LOW,
            [
                TakeProfitFibPer(fib_mark=1.382, vol_per=0.15),
                TakeProfitFibPer(fib_mark=1.618, vol_per=0.4),
                TakeProfitFibPer(fib_mark=2, vol_per=0.4),
                TakeProfitFibPer(fib_mark=2.618, vol_per=0.05),
                TakeProfitFibPer(fib_mark=3, vol_per=0),
            ],
        ),
        (
            ProfitPossibility.MARKET,
            [
                TakeProfitFibPer(fib_mark=1.382, vol_per=0.15),
                TakeProfitFibPer(fib_mark=1.618, vol_per=0.3),
                TakeProfitFibPer(fib_mark=2, vol_per=0.4),
                TakeProfitFibPer(fib_mark=2.618, vol_per=0.15),
                TakeProfitFibPer(fib_mark=3, vol_per=0),
            ],
        ),
        (
            ProfitPossibility.AGGRESSIVE,
            [
                TakeProfitFibPer(fib_mark=1.382, vol_per=0.1),
                TakeProfitFibPer(fib_mark=1.618, vol_per=0.2),
                TakeProfitFibPer(fib_mark=2, vol_per=0.45),
                TakeProfitFibPer(fib_mark=2.618, vol_per=0.15),
                TakeProfitFibPer(fib_mark=3, vol_per=0.1),
            ],
        ),
    ],
)
def test_get_profit_percentage_lst(tpp: ProfitPossibility, expect: list[float]):
    assert get_take_profit_fib_per_lst(tpp) == expect
