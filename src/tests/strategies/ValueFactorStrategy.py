import backtrader as bt

class PriceEarningsRatio(bt.Indicator):
    lines = ('pe_ratio',)
    params = (
        ('eps', 1.0),  # Earnings per share, default is 1.0
    )

    def __init__(self):
        self.lines.pe_ratio = self.data.close / self.params.eps

class PriceToBookRatio(bt.Indicator):
    lines = ('pb_ratio',)
    params = (
        ('book_value', 1.0),  # Book value per share, default is 1.0
    )

    def __init__(self):
        self.lines.pb_ratio = self.data.close / self.params.book_value

class ValueFactorStrategy(bt.Strategy):
    params = (
        ('eps', 1.0),
        ('book_value', 1.0),
    )

    def __init__(self):
        self.pe_ratio = PriceEarningsRatio(self.data, eps=self.params.eps)
        self.pb_ratio = PriceToBookRatio(self.data, book_value=self.params.book_value)

    def next(self):
        if self.pe_ratio.pe_ratio[0] < 15 and self.pb_ratio.pb_ratio[0] < 1.5:
            self.buy()
        elif self.pe_ratio.pe_ratio[0] > 25 or self.pb_ratio.pb_ratio[0] > 3:
            self.sell()
