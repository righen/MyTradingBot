import backtrader as bt

class BollingerBandsStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('devfactor', 2.0),
    )

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)

    def next(self):
        if self.data.close < self.bbands.bot:
            self.buy()
        elif self.data.close > self.bbands.top:
            self.sell()
