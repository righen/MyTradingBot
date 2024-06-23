import backtrader as bt

class StatisticalArbitrage(bt.Strategy):
    params = (
        ('lookback_period', 20),
    )

    def __init__(self):
        self.dataclose0 = self.datas[0].close
        self.dataclose1 = self.datas[1].close
        self.mean = bt.indicators.MovingAverageSimple((self.dataclose0 / self.dataclose1), period=self.params.lookback_period)
        self.stddev = bt.indicators.StandardDeviation((self.dataclose0 / self.dataclose1), period=self.params.lookback_period)

    def next(self):
        ratio = self.dataclose0[0] / self.dataclose1[0]
        upper = self.mean[0] + self.stddev[0]
        lower = self.mean[0] - self.stddev[0]

        if ratio > upper:
            self.sell(data=self.datas[0])
            self.buy(data=self.datas[1])
        elif ratio < lower:
            self.buy(data=self.datas[0])
            self.sell(data=self.datas[1])
