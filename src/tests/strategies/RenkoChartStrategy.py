import backtrader as bt

class RenkoIndicator(bt.Indicator):
    lines = ('renko_high', 'renko_low')
    params = (
        ('brick_size', 1),
    )

    def __init__(self):
        self.addminperiod(2)
        self.highs = []
        self.lows = []

    def next(self):
        close = self.data.close[0]
        if not self.highs or not self.lows:
            self.highs.append(close)
            self.lows.append(close)
            self.lines.renko_high[0] = close
            self.lines.renko_low[0] = close
        else:
            last_high = self.highs[-1]
            last_low = self.lows[-1]

            if close >= last_high + self.params.brick_size:
                self.highs.append(close)
                self.lows.append(last_low)
                self.lines.renko_high[0] = close
                self.lines.renko_low[0] = last_low
            elif close <= last_low - self.params.brick_size:
                self.highs.append(last_high)
                self.lows.append(close)
                self.lines.renko_high[0] = last_high
                self.lines.renko_low[0] = close
            else:
                self.lines.renko_high[0] = last_high
                self.lines.renko_low[0] = last_low

class RenkoChartStrategy(bt.Strategy):
    def __init__(self):
        self.renko = RenkoIndicator(self.data)

    def next(self):
        if self.renko.renko_high[0] > self.renko.renko_low[-1]:
            self.buy()
        elif self.renko.renko_low[0] < self.renko.renko_high[-1]:
            self.sell()
