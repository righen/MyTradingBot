import backtrader as bt

class FractalIndicator(bt.Indicator):
    lines = ('up_fractal', 'down_fractal')
    params = (('period', 2),)

    def __init__(self):
        self.addminperiod(self.params.period * 2 + 1)

    def next(self):
        if len(self) < self.params.period * 2 + 1:
            return

        mid_idx = self.params.period
        high_prices = [self.data.high[-i] for i in range(self.params.period * 2 + 1)]
        low_prices = [self.data.low[-i] for i in range(self.params.period * 2 + 1)]

        if high_prices[mid_idx] == max(high_prices):
            self.lines.up_fractal[0] = high_prices[mid_idx]
        else:
            self.lines.up_fractal[0] = float('nan')

        if low_prices[mid_idx] == min(low_prices):
            self.lines.down_fractal[0] = low_prices[mid_idx]
        else:
            self.lines.down_fractal[0] = float('nan')

class FractalIndicatorStrategy(bt.Strategy):
    def __init__(self):
        self.fractal = FractalIndicator(self.data)

    def next(self):
        if self.fractal.up_fractal[-1] and self.data.close[0] > self.fractal.up_fractal[-1]:
            self.buy()
        elif self.fractal.down_fractal[-1] and self.data.close[0] < self.fractal.down_fractal[-1]:
            self.sell()
