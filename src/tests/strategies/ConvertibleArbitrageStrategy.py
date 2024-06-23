import backtrader as bt

class ConvertibleArbitrageStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose_stock = self.datas[0].close
        self.dataclose_bond = self.datas[1].close

    def next(self):
        if self.dataclose_stock[0] > self.dataclose_bond[0]:
            self.sell(data=self.datas[0])
            self.buy(data=self.datas[1])
        elif self.dataclose_stock[0] < self.dataclose_bond[0]:
            self.buy(data=self.datas[0])
            self.sell(data=self.datas[1])
