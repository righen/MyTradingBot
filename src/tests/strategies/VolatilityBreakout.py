import backtrader as bt

class VolatilityBreakout(bt.Strategy):
    params = (
        ('atr_period', 14),
        ('atr_multiplier', 3.0),
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)

    def next(self):
        if self.data.close[0] > self.data.high[-1] + self.params.atr_multiplier * self.atr[0]:
            self.buy()
        elif self.data.close[0] < self.data.low[-1] - self.params.atr_multiplier * self.atr[0]:
            self.sell()
