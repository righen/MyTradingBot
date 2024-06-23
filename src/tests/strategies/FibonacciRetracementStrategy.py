import backtrader as bt

class FibonacciRetracementStrategy(bt.Strategy):
    def __init__(self):
        self.highest = bt.indicators.Highest(self.data.high, period=100)
        self.lowest = bt.indicators.Lowest(self.data.low, period=100)
        self.levels = [0.236, 0.382, 0.5, 0.618, 0.786]

    def next(self):
        range = self.highest[0] - self.lowest[0]
        levels = [self.lowest[0] + level * range for level in self.levels]

        if self.data.close[0] < levels[0]:
            self.buy()
        elif self.data.close[0] > levels[-1]:
            self.sell()
