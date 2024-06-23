import backtrader as bt

class IchimokuCloudBreakoutStrategy(bt.Strategy):
    def __init__(self):
        self.ichimoku = bt.indicators.Ichimoku()

    def next(self):
        if self.data.close[0] > self.ichimoku.senkou_span_a[0] and self.data.close[0] > self.ichimoku.senkou_span_b[0]:
            self.buy()
        elif self.data.close[0] < self.ichimoku.senkou_span_a[0] and self.data.close[0] < self.ichimoku.senkou_span_b[0]:
            self.sell()
