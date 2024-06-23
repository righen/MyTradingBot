import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the results
results_df = pd.read_csv('../../tests/strategy_results.csv', index_col=0)

# Dictionary mapping full strategy names to acronyms
strategy_acronyms = {
    'MovingAverageCrossover': 'MAC',
    'RSIStrategy': 'RSI',
    'BollingerBandsStrategy': 'BBS',
    'MeanReversion': 'MR',
    'Breakout': 'BO',
    'MACDStrategy': 'MACD',
    'MomentumStrategy': 'MS',
    'StochasticOscillatorStrategy': 'SOS',
    'ATRTrailingStopStrategy': 'ATRTS',
    'IchimokuCloudStrategy': 'ICS',
    'AdvancedMovingAverageCrossover': 'AMAC',
    'MACDHistogramDivergence': 'MACD-HD',
    'RSIandBollingerBandsCombo': 'RSI+BBS',
    'VolatilityBreakout': 'VB',
    'PairTrading': 'PT',
    'MeanReversionBollingerBands': 'MRBB',
    'AMAStrategy': 'AMA',
    'DualThrustStrategy': 'DTS',
    'KeltnerChannelStrategy': 'KCS',
    'DonchianChannelBreakout': 'DCB',
    'HeikinAshiStrategy': 'HAS',
    'VWAPStrategy': 'VWAP',
    'FibonacciRetracementStrategy': 'FRS',
    'MarketMakingStrategy': 'MMS',
    'StatisticalArbitrage': 'SA',
    'QuantitativeMomentumStrategy': 'QMS',
    'SeasonalityStrategy': 'SS',
    'MachineLearningStrategy': 'MLS',
    'SentimentAnalysisStrategy': 'SAS',
    'EventDrivenStrategy': 'EDS',
    'GAPTradingStrategy': 'GAPTS',
    'GridTradingStrategy': 'GTS',
    'RenkoChartStrategy': 'RCS',
    'FractalIndicatorStrategy': 'FIS',
    'SuperTrendStrategy': 'STS',
    'IchimokuCloudBreakoutStrategy': 'ICBS',
    'ButterflySpreadStrategy': 'BFS',
    'IronCondorStrategy': 'ICS',
    'MomentumReversalStrategy': 'MRS',
    'TriangleBreakoutStrategy': 'TBS',
    'MergerArbitrageStrategy': 'MAS',
    'ConvertibleArbitrageStrategy': 'CAS',
    'ValueFactorStrategy': 'VFS',
    'QualityFactorStrategy': 'QFS',
    'RiskParityStrategy': 'RPS',
    'LiquidityProvisionStrategy': 'LPS',
    'HighFrequencyTradingStrategy': 'HFTS',
    'SentimentBasedStrategy': 'SBS',
    'AlgorithmicTradingStrategy': 'ATS',
    'PortfolioOptimizationStrategy': 'POS',
    'AdaptiveStrategy': 'AS'
}

# Apply acronyms to the DataFrame
results_df.rename(index=strategy_acronyms, inplace=True)

# Calculate drawdown
results_df['Drawdown'] = results_df['Final Portfolio Value'] - results_df['Final Portfolio Value'].cummax()

# Calculate Sharpe Ratio
risk_free_rate = 0.01
results_df['Daily Return'] = results_df['Final Portfolio Value'].pct_change()
results_df['Sharpe Ratio'] = (results_df['Daily Return'].mean() - risk_free_rate) / results_df['Daily Return'].std()

# Calculate Sortino Ratio
negative_return = results_df['Daily Return'][results_df['Daily Return'] < 0]
results_df['Sortino Ratio'] = (results_df['Daily Return'].mean() - risk_free_rate) / negative_return.std()

# Calculate Win Rate
results_df['Win Rate'] = (results_df['Daily Return'] > 0).mean()

# Additional metrics
results_df['Max Drawdown'] = results_df['Drawdown'].min()
results_df['Cumulative Return'] = results_df['Final Portfolio Value'] / results_df['Final Portfolio Value'].iloc[0] - 1
results_df['Volatility'] = results_df['Daily Return'].std()

# Summary statistics
summary_stats = results_df.describe()

# Top 5 performers
top_5_strategies = results_df.sort_values(by='Final Portfolio Value', ascending=False).head(5)

# Bottom 5 performers
bottom_5_strategies = results_df.sort_values(by='Final Portfolio Value', ascending=True).head(5)

# Print summary statistics
print("Summary Statistics:")
print(summary_stats)

# Print top 5 performers
print("\nTop 5 Performers:")
print(top_5_strategies)

# Print bottom 5 performers
print("\nBottom 5 Performers:")
print(bottom_5_strategies)

# Print Sharpe Ratios
print("\nSharpe Ratios:")
print(results_df['Sharpe Ratio'])

# Plot the distribution of final portfolio values
plt.figure(figsize=(12, 6))
plt.hist(results_df['Final Portfolio Value'], bins=20, edgecolor='black')
plt.title('Distribution of Final Portfolio Values')
plt.xlabel('Final Portfolio Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Plot top and bottom performers
plt.figure(figsize=(12, 6))
plt.bar(top_5_strategies.index, top_5_strategies['Final Portfolio Value'], color='green', label='Top 5')
plt.bar(bottom_5_strategies.index, bottom_5_strategies['Final Portfolio Value'], color='red', label='Bottom 5')
plt.xticks(rotation=90)
plt.title('Top 5 and Bottom 5 Strategies')
plt.ylabel('Final Portfolio Value')
plt.legend()
plt.grid(True)
plt.show()

# Plot drawdown
plt.figure(figsize=(12, 6))
plt.plot(results_df.index, results_df['Drawdown'])
plt.title('Drawdown for Each Strategy')
plt.xlabel('Strategy')
plt.ylabel('Drawdown')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

# Plot Sharpe Ratio
plt.figure(figsize=(12, 6))
plt.bar(results_df.index, results_df['Sharpe Ratio'], color='lightblue')
plt.title('Sharpe Ratio by Strategy')
plt.xlabel('Strategy')
plt.ylabel('Sharpe Ratio')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

# Plot Sortino Ratio
plt.figure(figsize=(12, 6))
plt.bar(results_df.index, results_df['Sortino Ratio'], color='lightgreen')
plt.title('Sortino Ratio by Strategy')
plt.xlabel('Strategy')
plt.ylabel('Sortino Ratio')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

# Plot Max Drawdown
plt.figure(figsize=(12, 6))
plt.bar(results_df.index, results_df['Max Drawdown'], color='salmon')
plt.title('Maximum Drawdown by Strategy')
plt.xlabel('Strategy')
plt.ylabel('Max Drawdown')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

# Plot equity curve for top strategy
top_strategy = top_5_strategies.index[0]
plt.figure(figsize=(12, 6))
plt.plot(results_df['Date'], results_df[top_strategy])
plt.title(f'Equity Curve for Top Strategy: {top_strategy}')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.grid(True)
plt.show()

# Create a summary grid
summary_grid = results_df[['Final Portfolio Value', 'Max Drawdown', 'Sharpe Ratio', 'Sortino Ratio', 'Win Rate', 'Cumulative Return', 'Volatility']].sort_values(by='Final Portfolio Value', ascending=False)
print("\nSummary Grid:")
print(summary_grid)

# Save to CSV
summary_grid.to_csv('strategy_performance_summary.csv')

# Display the grid as a table
plt.figure(figsize=(14, 7))
plt.table(cellText=summary_grid.values,
          colLabels=summary_grid.columns,
          rowLabels=summary_grid.index,
          cellLoc='center',
          loc='center')
plt.axis('off')
plt.title('Strategy Performance Summary Grid')
plt.show()