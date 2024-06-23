# MyTradingBot

MyTradingBot is a Python-based trading bot that utilizes the Backtrader framework to implement and backtest various trading strategies on historical market data. This project aims to provide a robust environment for quantitative trading strategy development, testing, and analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Strategies](#strategies)
- [Analyzers](#analyzers)
- [Training Machine Learning Models](#training-machine-learning-models)
- [Examples](#examples)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Backtesting**: Test trading strategies on historical data.
- **Multiple Strategies**: Implement and test various trading strategies.
- **Performance Metrics**: Analyze strategies using key performance metrics like Sharpe ratio, Sortino ratio, maximum drawdown, win rate, etc.
- **Data Sources**: Fetch historical data from Yahoo Finance using the `yfinance` library.
- **Machine Learning**: Train and utilize machine learning models for trading strategies.
- **Extensibility**: Easily add new strategies and analyzers.

## Installation

1. **Clone the repository**

    ```sh
    git clone https://github.com/righen/MyTradingBot.git
    cd MyTradingBot
    ```

2. **Create a virtual environment (optional but recommended)**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run Backtrader Simulation**

    To run the backtrader simulation with all strategies:

    ```sh
    python src/tests/backtrader_simulation_all.py
    ```

2. **Analyze Strategy Results**

    To analyze the strategy results:

    ```sh
    python src/tests/strategies/analyze_strategy_results.py
    ```

3. **Train Machine Learning Models**

    To train machine learning models:

    ```sh
    python src/tests/train_models.py
    ```

## Strategies

The repository includes several trading strategies. Each strategy is defined in a separate Python file within the `src/tests/strategies` directory. Here are some of the included strategies:

- Moving Average Crossover
- RSI Strategy
- Bollinger Bands Strategy
- Mean Reversion
- Breakout
- MACD Strategy
- Momentum Strategy
- Stochastic Oscillator Strategy
- ATR Trailing Stop Strategy
- Ichimoku Cloud Strategy
- ... and many more.

## Analyzers

The bot uses various analyzers to assess the performance of the strategies:

- **PerformanceAnalyzer**: Custom analyzer to calculate various performance metrics.
- **DrawDown**: Measures the drawdown of the strategy.
- **SharpeRatio**: Calculates the Sharpe ratio.
- **SortinoRatio**: Custom analyzer to calculate the Sortino ratio.
- **AnnualReturn**: Calculates the annual return.
- **Returns**: Calculates the returns.

## Training Machine Learning Models

This repository also includes functionality for training machine learning models which can be integrated into trading strategies.

1. **Preparing the Data**

    The `train_models.py` script is used to prepare and train machine learning models on historical stock data. The script fetches data, computes features, and trains models.

    ```sh
    python src/tests/train_models.py
    ```

2. **Example Training Script (train_models.py)**

    ```python
    import yfinance as yf
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    import joblib

    def get_data(ticker):
        df = yf.download(ticker, start='2010-01-01')
        df['Return'] = df['Close'].pct_change()
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['Volatility'] = df['Close'].rolling(window=20).std()
        df.dropna(inplace=True)
        return df

    def train_model(df):
        X = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Return', 'MA5', 'MA20', 'Volatility']]
        y = (df['Return'] > 0).astype(int)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        joblib.dump(model, 'model.pkl')

    if __name__ == "__main__":
        data = get_data('AAPL')
        train_model(data)
    ```

## Examples

1. **Example Strategy File (MovingAverageCrossover.py)**

    ```python
    import backtrader as bt

    class MovingAverageCrossover(bt.Strategy):
        params = (
            ('fast_period', 10),
            ('slow_period', 30),
        )

        def __init__(self):
            self.fast_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.fast_period)
            self.slow_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.slow_period)

        def next(self):
            if self.fast_ma[0] > self.slow_ma[0] and self.fast_ma[-1] < self.slow_ma[-1]:
                self.buy()
            elif self.fast_ma[0] < self.slow_ma[0] and self.fast_ma[-1] > self.slow_ma[-1]:
                self.sell()
    ```

2. **Example of Running a Simulation**

    ```python
    from strategies import MovingAverageCrossover
    import backtrader as bt
    import yfinance as yf

    # Fetch historical data
    data = yf.download('AAPL', start='2010-01-01')

    # Prepare the data feed
    data_feed = bt.feeds.PandasData(dataname=data)

    # Set up the backtrader environment
    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    cerebro.addstrategy(MovingAverageCrossover)
    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission=0.005)

    # Run the strategy
    cerebro.run()
    cerebro.plot()
    ```

## Results

The results of the strategy simulations, including key performance metrics, are saved to a CSV file named `strategy_performance_metrics.csv`. This file includes metrics such as final portfolio value, maximum drawdown, Sharpe ratio, Sortino ratio, win rate, and more.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to modify and expand this README as per your project's requirements.
