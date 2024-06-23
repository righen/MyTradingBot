import backtrader as bt

class SuperTrend(bt.Indicator):
    lines = ('supertrend', 'final_ub', 'final_lb', 'basic_ub', 'basic_lb')
    params = (
        ('period', 10),
        ('multiplier', 3),
    )

    plotinfo = dict(subplot=False)

    def __init__(self):
        atr = bt.indicators.ATR(self.data, period=self.params.period)
        hl2 = (self.data.high + self.data.low) / 2
        self.l.basic_ub = hl2 + self.params.multiplier * atr
        self.l.basic_lb = hl2 - self.params.multiplier * atr

        self.l.final_ub = self.l.basic_ub
        self.l.final_lb = self.l.basic_lb

    def next(self):
        if self.data.close[-1] <= self.lines.final_ub[-1]:
            self.lines.final_ub[0] = max(self.lines.basic_ub[0], self.lines.final_ub[-1])
        else:
            self.lines.final_ub[0] = self.lines.basic_ub[0]

        if self.data.close[-1] >= self.lines.final_lb[-1]:
            self.lines.final_lb[0] = min(self.lines.basic_lb[0], self.lines.final_lb[-1])
        else:
            self.lines.final_lb[0] = self.lines.basic_lb[0]

        if self.data.close[0] > self.lines.final_ub[0]:
            self.lines.supertrend[0] = self.lines.final_lb[0]
        else:
            self.lines.supertrend[0] = self.lines.final_ub[0]


class SuperTrendStrategy(bt.Strategy):
    params = (
        ('period', 10),
        ('multiplier', 3),
    )

    def __init__(self):
        self.supertrend = SuperTrend(self.data, period=self.params.period, multiplier=self.params.multiplier)

    def next(self):
        if self.data.close[0] > self.supertrend[0]:
            if not self.position:
                self.buy()
        elif self.data.close[0] < self.supertrend[0]:
            if self.position:
                self.sell()
