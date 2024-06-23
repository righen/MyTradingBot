import backtrader as bt

class HeikinAshiStrategy(bt.Strategy):
    def __init__(self):
        self.ha_close = bt.indicators.HeikinAshi(self.data).ha_close

    def next(self):
        if self.data.close[0] > self.ha_close[0]:
            self.buy()
        elif self.data.close[0] < self.ha_close[0]:
            self.sell()
