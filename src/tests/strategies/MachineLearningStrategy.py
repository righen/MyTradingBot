import backtrader as bt
import joblib
import numpy as np

class MachineLearningStrategy(bt.Strategy):
    params = (
        ('ma5_period', 5),
        ('ma20_period', 20),
    )

    def __init__(self):
        self.model = joblib.load('../../models/xgboost_model.pkl')

        # Calculating moving averages
        self.ma5 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma5_period)
        self.ma20 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma20_period)

        # Calculating volatility
        self.volatility = bt.indicators.StandardDeviation(self.data.close, period=self.params.ma20_period)

    def next(self):
        # Calculate return
        return_value = (self.data.close[0] - self.data.close[-1]) / self.data.close[-1]

        # Collect the features
        features = [
            self.data.open[0],
            self.data.high[0],
            self.data.low[0],
            self.data.close[0],
            self.data.volume[0],
            return_value,
            self.ma5[0],
            self.ma20[0],
            self.volatility[0]
        ]

        # Reshape features to match the expected input format of the model
        features = np.array(features).reshape(1, -1)

        prediction = self.model.predict(features)
        if prediction == 1:
            self.buy()
        elif prediction == -1:
            self.sell()
