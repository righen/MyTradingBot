import backtrader as bt

class ATRTrailingStopStrategy(bt.Strategy):
    params = (
        ('atr_period', 14),
        ('atr_mult', 3),
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.buy_signal = False

    def next(self):
        if not self.position:
            if self.data.close[0] > self.data.close[-1]:
                self.buy()
                self.buy_signal = True
                self.stop_price = self.data.close[0] - self.params.atr_mult * self.atr[0]
        elif self.buy_signal:
            if self.data.close[0] < self.stop_price:
                self.sell()
                self.buy_signal = False
            else:
                self.stop_price = max(self.stop_price, self.data.close[0] - self.params.atr_mult * self.atr[0])
