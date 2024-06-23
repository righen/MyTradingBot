import pandas as pd
import numpy as np
import logging
from src.fetch_data import get_historical_data, save_to_csv, load_csv
from src.train_model import train_models, load_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_sample_data_from_csv(filepath):
    df = load_csv(filepath)
    if df is not None:
        df.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        }, inplace=True)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        logging.info(f"Loaded DataFrame:\n{df.head()}")
        return df
    else:
        logging.error("Failed to load data from CSV.")
        return None

def clean_data(df):
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    df.fillna(0, inplace=True)  # Ensure there are no NaN values left
    return df

def main():
    logging.info("Starting the trading bot...")

    symbol = 'AAPL'
    historical_file_path = f'data/historical/{symbol}_historical_data.csv'

    # Check if historical data exists
    historical_data = load_csv(historical_file_path)
    if historical_data is None:
        # Fetch historical data if not present
        logging.info(f"Fetching historical data for {symbol}...")
        historical_data = get_historical_data(symbol, outputsize='full')
        if historical_data is not None:
            save_to_csv(historical_data, historical_file_path)
            logging.info(f"Historical data saved to {historical_file_path}")
        else:
            logging.error("Failed to fetch historical data.")
            return

    # Train models
    logging.info("Training models...")
    xgboost_model_path = 'models/xgboost_model.pkl'
    lstm_model_path = 'models/lstm_model'  # Remove file extension, it will be added in train_lstm function
    lstm_history_path = 'models/lstm_model_history.json'
    df = load_data(historical_file_path)
    df = clean_data(df)
    train_models(df, xgboost_model_path, lstm_model_path, lstm_history_path)

if __name__ == "__main__":
    main()