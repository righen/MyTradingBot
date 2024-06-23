import backtrader as bt

class AlgorithmicTradingStrategy(bt.Strategy):
    def __init__(self):
        self.price = self.data.close

    def next(self):
        if self.price[0] > self.price[-1]:
            self.buy()
        elif self.price[0] < self.price[-1]:
            self.sell()
