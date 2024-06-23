import os
import requests
import pandas as pd

API_KEY = 'N6DQLQP9E6PV1551'
BASE_URL = 'https://www.alphavantage.co/query'

def get_historical_data(symbol, outputsize='full'):
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': outputsize,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'Time Series (Daily)' in data:
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        return df
    else:
        print("Error fetching data:", data)
        return None

def get_real_time_data(symbol, interval='1min'):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if f'Time Series ({interval})' in data:
        df = pd.DataFrame.from_dict(data[f'Time Series ({interval})'], orient='index')
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        return df
    else:
        print("Error fetching data:", data)
        return None

def save_to_csv(df, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=True)
    print(f'Data saved to {file_path}')

def load_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, index_col=0, parse_dates=True)
    return None
