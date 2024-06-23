import backtrader as bt

import backtrader as bt

class DonchianChannels(bt.Indicator):
    lines = ('dch', 'dcl')
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.addminperiod(self.params.period)
        self.l.dch = bt.indicators.Highest(self.data.high, period=self.params.period)
        self.l.dcl = bt.indicators.Lowest(self.data.low, period=self.params.period)

class DonchianChannelBreakout(bt.Strategy):
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.donchian = DonchianChannels(self.data, period=self.params.period)

    def next(self):
        if self.data.close[0] > self.donchian.dch[0]:
            self.buy()
        elif self.data.close[0] < self.donchian.dcl[0]:
            self.sell()

