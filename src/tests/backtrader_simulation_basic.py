import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

class SmaCross(bt.Strategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=50)
        sma2 = bt.ind.SMA(period=100)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()

        elif self.crossover < 0:
            self.close()

# Create a cerebro entity
cerebro = bt.Cerebro()

# Download historical data from Yahoo Finance
df = yf.download('AAPL', start='2010-01-01')

symbol = 'AAPL'
historical_file_path = f'../data/historical/{symbol}_historical_data.csv'

# Use Backtrader's GenericCSVData Data Feed
feed = bt.feeds.GenericCSVData(
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

cerebro.addstrategy(SmaCross)

cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(commission=0.005)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)

cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='areturn')

# Add the data feed to Cerebro
cerebro.adddata(feed)

# Run the strategy
results = cerebro.run()

a = results[0].analyzers.areturn.get_analysis()

# Plot the result
figure = cerebro.plot()[0][0]

# Save the plot to a file
figure.savefig('backtrader_plot.png')

print("Plot saved as 'backtrader_plot.png'")

