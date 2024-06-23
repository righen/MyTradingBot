import backtrader as bt

class RiskParityStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = [data.close for data in self.datas]
        self.weights = [1.0 / len(self.datas)] * len(self.datas)

    def next(self):
        portfolio_value = sum([self.weights[i] * self.dataclose[i][0] for i in range(len(self.datas))])
        for i, data in enumerate(self.datas):
            target_value = portfolio_value * self.weights[i]
            current_value = data.close[0]
            if current_value < target_value:
                self.buy(data=data)
            elif current_value > target_value:
                self.sell(data=data)
