import backtrader as bt

class QuantitativeMomentumStrategy(bt.Strategy):
    params = (
        ('momentum_period', 12),
    )

    def __init__(self):
        self.momentum = bt.indicators.Momentum(self.data.close, period=self.params.momentum_period)

    def next(self):
        if self.momentum[0] > 100:
            self.buy()
        elif self.momentum[0] < 100:
            self.sell()
