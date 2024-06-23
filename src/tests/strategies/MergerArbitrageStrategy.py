import backtrader as bt

class MergerArbitrageStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose0 = self.datas[0].close
        self.dataclose1 = self.datas[1].close

    def next(self):
        if self.dataclose0[0] > self.dataclose1[0]:
            self.sell(data=self.datas[0])
            self.buy(data=self.datas[1])
        elif self.dataclose0[0] < self.dataclose1[0]:
            self.buy(data=self.datas[0])
            self.sell(data=self.datas[1])
