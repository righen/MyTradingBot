import logging
import backtrader as bt
from datetime import datetime
import pandas as pd
from src.predict import load_xgboost_model, load_lstm_model
import os
from src.strategy import ModelBasedStrategy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backtrader_simulation():
    logging.info("Starting the trading bot...")

    # Load the first record from the historical CSV
    symbol = 'AAPL'
    historical_file_path = f'data/historical/{symbol}_historical_data.csv'

    # Use Backtrader's GenericCSVData Data Feed
    data_feed = bt.feeds.GenericCSVData(
        dataname=historical_file_path,
        dtformat=('%Y-%m-%d'),  # Assuming your date format is YYYY-MM-DD
        datetime=0,  # Column index for date
        open=1,  # Column index for open
        high=2,  # Column index for high
        low=3,  # Column index for low
        close=4,  # Column index for close
        volume=5,  # Column index for volume
        openinterest=-1  # No open interest column in CSV
    )

    if data_feed is not None:
        logging.info("Data feed details:\n%s", data_feed)

        # Initialize Backtrader engine
        cerebro = bt.Cerebro()
        cerebro.adddata(data_feed)
        cerebro.broker.setcash(10000.0)

        xgboost_model_path = 'models/xgboost_model.pkl'
        lstm_model_path = 'models/lstm_model'  # Remove file extension, it will be added in train_lstm function

        # Load trained models
        logging.info("Loading trained models...")
        xgboost_model = load_xgboost_model(xgboost_model_path)
        lstm_model = load_lstm_model(lstm_model_path + '.keras')

        cerebro.addstrategy(ModelBasedStrategy, xgboost_model=xgboost_model, lstm_model=lstm_model)

        # Add analyzers
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharperatio')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeanalyzer')
        cerebro.addanalyzer(bt.analyzers.Transactions, _name='transactions')
        cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='timereturn')

        logging.info("Starting Backtrader engine run...")
        strategies = cerebro.run()
        logging.info("Backtrader engine run complete.")

        # Save predictions to a CSV file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = 'results'
        os.makedirs(output_dir, exist_ok=True)
        predictions_file = os.path.join(output_dir, f'predictions_{timestamp}.csv')
        metrics_file = os.path.join(output_dir, f'metrics_{timestamp}.csv')

        # Store and log the results
        final_results = []
        all_predictions = []
        for strat in strategies:
            all_predictions.extend(strat.predictions)

            final_results.append({
                'ending_value': cerebro.broker.getvalue(),
                'ending_cash': cerebro.broker.getcash(),
                'predictions': strat.predictions  # Store the predictions
            })

        predictions_df = pd.DataFrame(all_predictions)
        predictions_df.to_csv(predictions_file, index=False)
        logging.info("Predictions saved to %s", predictions_file)

        # Extract and save the performance metrics
        strategy = strategies[0]
        analyzers = strategy.analyzers

        metrics = {
            'Sharpe Ratio': analyzers.sharperatio.get_analysis()['sharperatio'],
            'Drawdown': analyzers.drawdown.get_analysis(),
            'Trade Analyzer': analyzers.tradeanalyzer.get_analysis(),
            'Transactions': analyzers.transactions.get_analysis(),
            'Time Return': analyzers.timereturn.get_analysis()
        }

        metrics_flat = {
            'Sharpe Ratio': metrics['Sharpe Ratio'],
            'Drawdown': metrics['Drawdown']['drawdown'],
            'Max Drawdown': metrics['Drawdown']['max']['drawdown'],
            'Total Trades': metrics['Trade Analyzer']['total']['total'],
            'Total Open': metrics['Trade Analyzer']['total']['open'],
            'Total Closed': metrics['Trade Analyzer']['total']['closed'],
            'Total Won': metrics['Trade Analyzer']['won']['total'],
            'Total Lost': metrics['Trade Analyzer']['lost']['total'],
            'Net P/L': metrics['Trade Analyzer']['pnl']['net']['total']
        }

        metrics_df = pd.DataFrame([metrics_flat])
        metrics_df.to_csv(metrics_file, index=False)
        logging.info("Metrics saved to %s", metrics_file)

        # Plot the results
        try:
            cerebro.plot()
        except Exception as e:
            logging.error(f"Error during plotting: {e}")

        logging.info("Final results: %s", final_results)
    else:
        logging.error("Failed to create data feed.")

if __name__ == "__main__":
    backtrader_simulation()
