import os
import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
import joblib
import xgboost as xgb
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

def load_data(file_path):
    return pd.read_csv(file_path, index_col=0, parse_dates=True)

def add_features(df):
    df['return'] = df['4. close'].pct_change()
    df['ma_5'] = df['4. close'].rolling(window=5).mean()
    df['ma_20'] = df['4. close'].rolling(window=20).mean()
    df['volatility'] = df['return'].rolling(window=20).std()
    df.dropna(inplace=True)
    return df

def train_xgboost(df, model_path):
    df['target'] = df['4. close'].shift(-1)
    df.dropna(inplace=True)

    X = df[['1. open', '2. high', '3. low', '4. close', '5. volume', 'return', 'ma_5', 'ma_20', 'volatility']]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, predictions)
    mape = mean_absolute_percentage_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f'XGBoost Model MSE: {mse}')
    print(f'XGBoost Model RMSE: {rmse}')
    print(f'XGBoost Model MAE: {mae}')
    print(f'XGBoost Model MAPE: {mape * 100}%')
    print(f'XGBoost Model R²: {r2}')

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f'XGBoost model saved to {model_path}')

def plot_history(history):
    plt.figure(figsize=(12, 6))
    plt.plot(history['loss'], label='Training Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss over Epochs')
    plt.legend()
    plt.show()

def save_history(history, filepath):
    with open(filepath, 'w') as file:
        json.dump(history, file)

def load_history(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def train_lstm(df, model_path, history_path):
    df['target'] = df['4. close'].shift(-1)
    df.dropna(inplace=True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['4. close']])

    train_size = int(len(scaled_data) * 0.8)
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size:]

    def create_dataset(dataset, time_step=1):
        X, y = [], []
        for i in range(len(dataset) - time_step - 1):
            X.append(dataset[i:(i + time_step), 0])
            y.append(dataset[i + time_step, 0])
        return np.array(X), np.array(y)

    time_step = 60
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    print(f'X_train shape: {X_train.shape}')
    print(f'y_train shape: {y_train.shape}')
    print(f'X_test shape: {X_test.shape}')
    print(f'y_test shape: {y_test.shape}')

    if X_train.shape[0] == 0 or X_test.shape[0] == 0:
        print("Error: Not enough data to create training and testing datasets with the given time_step.")
        return

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(time_step, 1)),
        tf.keras.layers.LSTM(50, return_sequences=True),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.LSTM(50, return_sequences=False),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(25),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Load previous history if exists
    initial_epoch = 0
    if os.path.exists(history_path):
        history_data = load_history(history_path)
        initial_epoch = len(history_data['loss'])
        model.load_weights(model_path + '_weights.weights.h5')  # Ensure the correct file extension
    else:
        history_data = {'loss': [], 'val_loss': []}

    # EarlyStopping and ModelCheckpoint callbacks
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(model_path + '_weights.weights.h5', save_best_only=True,
                                                          save_weights_only=True)

    try:
        history = model.fit(X_train, y_train,
                            validation_data=(X_test, y_test),
                            batch_size=32,
                            epochs=2000,  # Set a high number of epochs
                            initial_epoch=initial_epoch,
                            callbacks=[early_stopping, model_checkpoint])

        # Update history
        history_data['loss'].extend(history.history.get('loss', []))
        history_data['val_loss'].extend(history.history.get('val_loss', []))
        save_history(history_data, history_path)

        predictions = model.predict(X_test)
        y_test_scaled_back = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
        predictions_scaled_back = scaler.inverse_transform(predictions).flatten()

        mse = mean_squared_error(y_test_scaled_back, predictions_scaled_back)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test_scaled_back, predictions_scaled_back)
        mape = mean_absolute_percentage_error(y_test_scaled_back, predictions_scaled_back)
        r2 = r2_score(y_test_scaled_back, predictions_scaled_back)

        print(f'LSTM Model MSE: {mse}')
        print(f'LSTM Model RMSE: {rmse}')
        print(f'LSTM Model MAE: {mae}')
        print(f'LSTM Model MAPE: {mape * 100}%')
        print(f'LSTM Model R²: {r2}')

        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save(model_path + '.keras')
        print(f'LSTM model saved to {model_path}.keras')

        # Plot the training history
        plot_history(history_data)

    except Exception as e:
        print(f"An error occurred during LSTM training: {e}")
        return

def train_models(df, xgboost_path, lstm_path, lstm_history_path):
    df = add_features(df)
    Parallel(n_jobs=4)(
        [delayed(train_xgboost)(df, xgboost_path),
         delayed(train_lstm)(df, lstm_path, lstm_history_path)]
    )
