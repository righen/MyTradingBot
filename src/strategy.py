import backtrader as bt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

class ModelBasedStrategy(bt.Strategy):
    params = (
        ('time_step', 60),
    )

    def __init__(self, xgboost_model, lstm_model):
        self.xgboost_model = xgboost_model
        self.lstm_model = lstm_model
        self.time_step = self.params.time_step
        self.data_close = self.datas[0].close

        self.close_prices = []
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        self.predictions = []  # Store predictions

    def next(self):
        # Append the latest closing price
        self.close_prices.append(self.data_close[0])
        if len(self.close_prices) < self.time_step:
            return  # Not enough data yet

        if len(self.close_prices) > self.time_step:
            self.close_prices.pop(0)  # Remove oldest price to maintain time_step size

        # Retrieve and log individual values
        open_price = self.datas[0].open[0]
        high_price = self.datas[0].high[0]
        low_price = self.datas[0].low[0]
        close_price = self.datas[0].close[0]
        volume = self.datas[0].volume[0]
        ret = self.data_close[0] / self.data_close[-1] - 1
        ma_5 = sum(self.data_close.get(size=5)) / 5 if len(self.data_close.get(size=5)) == 5 else np.nan
        ma_20 = sum(self.data_close.get(size=20)) / 20 if len(self.data_close.get(size=20)) == 20 else np.nan
        volatility = np.std(self.data_close.get(size=20)) if len(self.data_close.get(size=20)) == 20 else np.nan

        if np.isnan(open_price) or np.isnan(high_price) or np.isnan(low_price) or np.isnan(close_price) or \
           np.isnan(volume) or np.isnan(ret) or np.isnan(ma_5) or np.isnan(ma_20) or np.isnan(volatility):
            return  # Skip if any data is missing

        # Prepare the data for XGBoost prediction
        df = pd.DataFrame({
            '1. open': [open_price],
            '2. high': [high_price],
            '3. low': [low_price],
            '4. close': [close_price],
            '5. volume': [volume],
            'return': [ret],
            'ma_5': [ma_5],
            'ma_20': [ma_20],
            'volatility': [volatility]
        })

        # XGBoost prediction
        xgboost_pred = self.xgboost_model.predict(df)[0]

        # Prepare the data for LSTM prediction
        scaled_data = self.scaler.fit_transform(np.array(self.close_prices).reshape(-1, 1))
        X = np.array([scaled_data])
        X = X.reshape((1, self.time_step, 1))

        # LSTM prediction
        lstm_pred = self.lstm_model.predict(X)[0][0]
        lstm_pred = self.scaler.inverse_transform([[lstm_pred]])[0][0]

        # Store the predictions
        self.predictions.append({
            'datetime': self.datas[0].datetime.date(0),
            'close': self.data_close[0],
            'xgboost_pred': xgboost_pred,
            'lstm_pred': lstm_pred
        })

        # Generate signals based on model predictions
        if lstm_pred > self.data_close[0] and xgboost_pred > self.data_close[0]:
            self.buy()
        elif lstm_pred < self.data_close[0] and xgboost_pred < self.data_close[0]:
            self.sell()