import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)

    def next(self):
        if self.rsi < self.params.rsi_oversold:
            self.buy()
        elif self.rsi > self.params.rsi_overbought:
            self.sell()
