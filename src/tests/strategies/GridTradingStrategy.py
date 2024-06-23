import backtrader as bt

class GridTradingStrategy(bt.Strategy):
    params = (
        ('grid_size', 10),
        ('max_position_size', 100),
    )

    def __init__(self):
        self.price_levels = []
        self.custom_position = 0  # Renamed to avoid conflict with the built-in position attribute

    def next(self):
        if not self.price_levels:
            self.price_levels = [self.data.close[0] + i * self.params.grid_size for i in range(-5, 6)]

        for level in self.price_levels:
            if self.data.close[0] > level and self.custom_position < self.params.max_position_size:
                self.buy()
                self.custom_position += 1
            elif self.data.close[0] < level and self.custom_position > -self.params.max_position_size:
                self.sell()
                self.custom_position -= 1
