import backtrader as bt

class MomentumReversalStrategy(bt.Strategy):
    params = (
        ('momentum_period', 20),
        ('reversal_period', 5),
    )

    def __init__(self):
        self.momentum = bt.indicators.Momentum(self.data.close, period=self.params.momentum_period)

    def next(self):
        if self.momentum[0] > 100:
            self.buy()
        elif self.momentum[0] < 100:
            self.sell()
