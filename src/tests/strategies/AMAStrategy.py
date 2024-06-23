import backtrader as bt

class AMAStrategy(bt.Strategy):
    params = (
        ('fast', 2),
        ('slow', 30),
        ('period', 10),
    )

    def __init__(self):
        self.ama = bt.indicators.AdaptiveMovingAverage(self.data.close, period=self.params.period, fast=self.params.fast, slow=self.params.slow)

    def next(self):
        if self.data.close[0] > self.ama[0]:
            self.buy()
        elif self.data.close[0] < self.ama[0]:
            self.sell()
