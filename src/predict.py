import pandas as pd
import joblib
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def load_xgboost_model(model_path):
    return joblib.load(model_path)

def load_lstm_model(model_path):
    return tf.keras.models.load_model(model_path)

def make_xgboost_prediction(model, df):
    X = df[['1. open', '2. high', '3. low', '4. close', '5. volume', 'return', 'ma_5', 'ma_20', 'volatility']]
    prediction = model.predict(X)
    df['xgboost_prediction'] = prediction
    return df

def make_lstm_prediction(model, df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['4. close']])

    def create_dataset(dataset, time_step=1):
        X = []
        for i in range(len(dataset) - time_step):
            X.append(dataset[i:(i + time_step), 0])
        return np.array(X)

    time_step = 60
    X = create_dataset(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    prediction = model.predict(X)
    prediction = scaler.inverse_transform(prediction)
    df['lstm_prediction'] = np.nan
    df.iloc[time_step:, df.columns.get_loc('lstm_prediction')] = prediction.flatten()
    return df

def save_predictions(df, file_path):
    df.to_csv(file_path, index=True)
    print(f'Predictions saved to {file_path}')
