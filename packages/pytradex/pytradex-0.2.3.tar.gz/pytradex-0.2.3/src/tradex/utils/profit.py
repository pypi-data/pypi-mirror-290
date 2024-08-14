from tradex.constants.enuming import Direction, ProfitPossibility
from tradex.constants.listting import TP_FIB, TP_PER_AGGRESSIVE, TP_PER_LOW, TP_PER_MARKET
from tradex.models.order import OrderProfitFormSimple
from tradex.models.take_profit import TakeProfit, TakeProfitFibPer
from tradex.utils.fibonacci import fib_retrace_standalone


def get_take_profit_fib_per_lst(tpp: ProfitPossibility) -> list[TakeProfitFibPer]:
    possibility = None
    if tpp == ProfitPossibility.MARKET:
        possibility = TP_PER_MARKET
    elif tpp == ProfitPossibility.LOW:
        possibility = TP_PER_LOW
    elif tpp == ProfitPossibility.AGGRESSIVE:
        possibility = TP_PER_AGGRESSIVE
    else:
        raise ValueError("Parameter %s is unacceptable", tpp)
    return [TakeProfitFibPer(fib_mark=fib, vol_per=per) for fib, per in zip(TP_FIB, possibility, strict=False)]


def take_profit_list(
    *, order: OrderProfitFormSimple, tpp: ProfitPossibility | None = ProfitPossibility.MARKET
) -> list[TakeProfit]:
    take_profit_fib_per = get_take_profit_fib_per_lst(tpp)

    return [
        TakeProfit(
            volume=round(order.size * tpfp.vol_per, 3),
            price=fib_retrace_standalone(zero=order.zero_mark, middle=order.middle_mark, fib_val=tpfp.fib_mark),
            percentage=tpfp.vol_per,
        )
        for tpfp in take_profit_fib_per
    ]


def take_profit_total(*, order: OrderProfitFormSimple, take_profits: list[TakeProfit]) -> float:
    product_size = order.size / order.price
    sell_total_size = sum([product_size * tp.percentage * tp.price for tp in take_profits])
    if order.order_type == Direction.LONG:
        return round(sell_total_size - order.size, 2)
    else:  # noqa
        return round(order.size - sell_total_size, 2)


# def stop_loss_cal(order: OrderProfitFormSimple,
#                   stop_loss: list[StopLoss]) -> float:
#     total_price = sum([sl.volume * sl.price for sl in stop_loss])
#     return round(order.order_price - total_price, 2)
