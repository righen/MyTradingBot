import backtrader as bt

class KeltnerChannel(bt.Indicator):
    lines = ('mid', 'top', 'bot')
    params = (
        ('period', 20),
        ('mult', 1.5),
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.params.period)
        self.mid = bt.indicators.SMA(self.data.close, period=self.params.period)

    def next(self):
        self.lines.mid[0] = self.mid[0]
        self.lines.top[0] = self.mid[0] + self.params.mult * self.atr[0]
        self.lines.bot[0] = self.mid[0] - self.params.mult * self.atr[0]

class KeltnerChannelStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('mult', 1.5),
    )

    def __init__(self):
        self.keltner = KeltnerChannel(self.data, period=self.params.period, mult=self.params.mult)

    def next(self):
        if self.data.close[0] > self.keltner.top[0]:
            self.buy()
        elif self.data.close[0] < self.keltner.bot[0]:
            self.sell()

