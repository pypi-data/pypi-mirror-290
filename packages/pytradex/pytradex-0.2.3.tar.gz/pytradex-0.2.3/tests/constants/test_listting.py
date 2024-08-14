import pytest

from tradex.constants.listting import TP_FIB, TP_PER_AGGRESSIVE, TP_PER_LOW, TP_PER_MARKET


@pytest.mark.parametrize(
    ("tp_fib", "tp_per"),
    [
        (TP_FIB, TP_PER_MARKET),
        (TP_FIB, TP_PER_LOW),
        (TP_FIB, TP_PER_AGGRESSIVE),
    ],
)
def test_profit_percentage_same_size(tp_fib: list[float], tp_per: list[float]):
    assert len(tp_fib) == len(tp_per)


@pytest.mark.parametrize(
    "tp_fib",
    [
        TP_PER_MARKET,
        TP_PER_LOW,
        TP_PER_AGGRESSIVE,
    ],
)
def test_tp_profit_100_percentage(tp_fib: list[float]):
    assert sum(tp_fib) == 1.0, f"{tp_fib} must equal to one"
