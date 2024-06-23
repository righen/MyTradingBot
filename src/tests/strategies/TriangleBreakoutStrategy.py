import backtrader as bt

class TriangleBreakoutStrategy(bt.Strategy):
    def __init__(self):
        self.highest = bt.indicators.Highest(self.data.high, period=14)
        self.lowest = bt.indicators.Lowest(self.data.low, period=14)

    def next(self):
        if self.data.close[0] > self.highest[-1]:
            self.buy()
        elif self.data.close[0] < self.lowest[-1]:
            self.sell()
