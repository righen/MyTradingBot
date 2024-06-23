import backtrader as bt

class MomentumStrategy(bt.Strategy):
    params = (
        ('period', 14),
    )

    def __init__(self):
        self.momentum = bt.indicators.Momentum(self.data.close, period=self.params.period)

    def next(self):
        if self.momentum[0] > 100:
            self.buy()
        elif self.momentum[0] < 100:
            self.sell()
