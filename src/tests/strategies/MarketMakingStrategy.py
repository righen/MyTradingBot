import backtrader as bt

class MarketMakingStrategy(bt.Strategy):
    def __init__(self):
        self.price = self.data.close

    def next(self):
        bid_price = self.price[0] - 0.01
        ask_price = self.price[0] + 0.01
        self.buy(price=bid_price)
        self.sell(price=ask_price)
