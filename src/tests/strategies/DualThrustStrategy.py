import backtrader as bt

class DualThrustStrategy(bt.Strategy):
    params = (
        ('k1', 0.5),
        ('k2', 0.5),
        ('period', 20),
    )

    def __init__(self):
        self.highest = bt.indicators.Highest(self.data.high, period=self.params.period)
        self.lowest = bt.indicators.Lowest(self.data.low, period=self.params.period)
        self.range = self.highest - self.lowest

    def next(self):
        upper_bound = self.data.open[0] + self.params.k1 * self.range[0]
        lower_bound = self.data.open[0] - self.params.k2 * self.range[0]

        if self.data.close[0] > upper_bound:
            self.buy()
        elif self.data.close[0] < lower_bound:
            self.sell()
