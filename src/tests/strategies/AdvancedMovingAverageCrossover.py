import backtrader as bt

class AdvancedMovingAverageCrossover(bt.Strategy):
    params = (
        ('fast', 10),
        ('medium', 20),
        ('slow', 50),
    )

    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.fast)
        self.medium_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.medium)
        self.slow_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        self.crossover_medium = bt.indicators.CrossOver(self.medium_ma, self.slow_ma)

    def next(self):
        if self.crossover > 0 and self.crossover_medium > 0:
            self.buy()
        elif self.crossover < 0 and self.crossover_medium < 0:
            self.sell()
