import backtrader as bt

class StochasticOscillatorStrategy(bt.Strategy):
    def __init__(self):
        self.stochastic = bt.indicators.Stochastic()

    def next(self):
        if self.stochastic.percK[0] > self.stochastic.percD[0] and self.stochastic.percK[-1] <= self.stochastic.percD[-1]:
            self.buy()
        elif self.stochastic.percK[0] < self.stochastic.percD[0] and self.stochastic.percK[-1] >= self.stochastic.percD[-1]:
            self.sell()
