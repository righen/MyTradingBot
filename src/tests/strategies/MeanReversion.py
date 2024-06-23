import backtrader as bt

class MeanReversion(bt.Strategy):
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.period)

    def next(self):
        if self.data.close[0] < self.sma[0]:
            self.buy()
        elif self.data.close[0] > self.sma[0]:
            self.sell()
