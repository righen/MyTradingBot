import backtrader as bt

class MACDHistogramDivergence(bt.Strategy):
    def __init__(self):
        self.macd = bt.indicators.MACD(self.data.close)
        self.macdhist = bt.indicators.MACDHisto(self.data.close)

    def next(self):
        if self.macdhist.histo[0] > 0 and self.macdhist.histo[-1] <= 0:
            self.buy()
        elif self.macdhist.histo[0] < 0 and self.macdhist.histo[-1] >= 0:
            self.sell()
