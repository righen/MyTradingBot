import backtrader as bt

class GAPTradingStrategy(bt.Strategy):
    def __init__(self):
        self.order = None

    def next(self):
        if self.order:
            return

        if self.data.open[0] > self.data.close[-1] * 1.02:
            self.order = self.buy()
        elif self.data.open[0] < self.data.close[-1] * 0.98:
            self.order = self.sell()
