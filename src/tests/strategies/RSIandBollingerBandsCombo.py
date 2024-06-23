import backtrader as bt

class RSIandBollingerBandsCombo(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
        ('bb_period', 20),
        ('bb_dev', 2.0),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.bbands = bt.indicators.BollingerBands(self.data.close, period=self.params.bb_period, devfactor=self.params.bb_dev)

    def next(self):
        if self.rsi < self.params.rsi_oversold and self.data.close < self.bbands.bot:
            self.buy()
        elif self.rsi > self.params.rsi_overbought and self.data.close > self.bbands.top:
            self.sell()
