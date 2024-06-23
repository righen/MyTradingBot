import backtrader as bt

class MeanReversionBollingerBands(bt.Strategy):
    params = (
        ('bb_period', 20),
        ('bb_dev', 2.0),
    )

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(self.data.close, period=self.params.bb_period, devfactor=self.params.bb_dev)

    def next(self):
        if self.data.close < self.bbands.bot:
            self.buy()
        elif self.data.close > self.bbands.mid:
            self.sell()
