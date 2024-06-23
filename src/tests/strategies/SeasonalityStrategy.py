import backtrader as bt

class SeasonalityStrategy(bt.Strategy):
    def __init__(self):
        pass

    def next(self):
        current_month = self.datas[0].datetime.date(0).month
        if current_month == 11:  # Assume November is a good month to buy
            self.buy()
        elif current_month == 5:  # Assume May is a good month to sell
            self.sell()
