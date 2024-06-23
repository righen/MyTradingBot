import backtrader as bt

import backtrader as bt

class VolumeWeightedAveragePrice(bt.Indicator):
    lines = ('vwap',)
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.addminperiod(self.params.period)
        self.volsum = bt.indicators.SumN(self.data.volume, period=self.params.period)
        self.pvsum = bt.indicators.SumN(self.data.volume * self.data.close, period=self.params.period)

    def next(self):
        self.lines.vwap[0] = self.pvsum[0] / self.volsum[0]


class VWAPStrategy(bt.Strategy):
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.vwap = VolumeWeightedAveragePrice(self.data, period=self.params.period)

    def next(self):
        if self.data.close[0] > self.vwap[0]:
            self.buy()
        elif self.data.close[0] < self.vwap[0]:
            self.sell()
