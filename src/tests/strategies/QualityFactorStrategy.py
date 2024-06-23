import backtrader as bt

class ReturnOnAssets(bt.Indicator):
    lines = ('roa',)
    params = (
        ('net_income', 1.0),  # Net income, default is 1.0
        ('total_assets', 1.0),  # Total assets, default is 1.0
    )

    def __init__(self):
        self.lines.roa = self.params.net_income / self.params.total_assets

class ReturnOnEquity(bt.Indicator):
    lines = ('roe',)
    params = (
        ('net_income', 1.0),  # Net income, default is 1.0
        ('shareholder_equity', 1.0),  # Shareholder equity, default is 1.0
    )

    def __init__(self):
        self.lines.roe = self.params.net_income / self.params.shareholder_equity

class QualityFactorStrategy(bt.Strategy):
    class QualityFactorStrategy(bt.Strategy):
        params = (
            ('net_income', 1.0),
            ('total_assets', 1.0),
            ('shareholder_equity', 1.0),
        )

        def __init__(self):
            self.roa = ReturnOnAssets(net_income=self.params.net_income, total_assets=self.params.total_assets)
            self.roe = ReturnOnEquity(net_income=self.params.net_income,
                                      shareholder_equity=self.params.shareholder_equity)

        def next(self):
            if self.roa.roa[0] > 5 and self.roe.roe[0] > 10:
                self.buy()
            elif self.roa.roa[0] < 2 or self.roe.roe[0] < 5:
                self.sell()
