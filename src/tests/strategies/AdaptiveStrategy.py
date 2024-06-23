import backtrader as bt

class AdaptiveStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.data.close
        self.sma = bt.indicators.SimpleMovingAverage(self.dataclose, period=30)
        self.atr = bt.indicators.AverageTrueRange(self.data)

    def next(self):
        if self.dataclose[0] > self.sma[0] and self.atr[0] > 1.0:
            self.buy()
        elif self.dataclose[0] < self.sma[0] and self.atr[0] > 1.0:
            self.sell()
