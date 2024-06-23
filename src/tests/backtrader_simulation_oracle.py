import backtrader as bt
import datetime
from strategies import (
    TestStrategy,
    TestStrategy2,
    TestStrategy3,
    TestStrategy4,
    MovingAverageCrossover,
    RSIStrategy,
    BollingerBandsStrategy,
    MeanReversion,
    Breakout,
    MACDStrategy,
    MomentumStrategy,
    StochasticOscillatorStrategy,
    ATRTrailingStopStrategy,
    IchimokuCloudStrategy,
    AdvancedMovingAverageCrossover,
    MACDHistogramDivergence,
    RSIandBollingerBandsCombo,
    VolatilityBreakout,
    PairTrading,
    MeanReversionBollingerBands,
    AMAStrategy,
    DualThrustStrategy,
    KeltnerChannelStrategy,
    DonchianChannelBreakout,
    HeikinAshiStrategy,
    VWAPStrategy,
    FibonacciRetracementStrategy,
    MarketMakingStrategy,
    StatisticalArbitrage,
    QuantitativeMomentumStrategy,
    SeasonalityStrategy,
    MachineLearningStrategy,
    SentimentAnalysisStrategy,
    EventDrivenStrategy,
    GAPTradingStrategy,
    GridTradingStrategy,
    IchimokuCloudBreakoutStrategy,
    ButterflySpreadStrategy,
    IronCondorStrategy,
    MomentumReversalStrategy,
    TriangleBreakoutStrategy,
    RenkoChartStrategy,
    FractalIndicatorStrategy,
    SuperTrendStrategy,
    MergerArbitrageStrategy,
    ConvertibleArbitrageStrategy,
    ValueFactorStrategy,
    QualityFactorStrategy,
    RiskParityStrategy,
    LiquidityProvisionStrategy,
    HighFrequencyTradingStrategy,
    SentimentBasedStrategy,
    AlgorithmicTradingStrategy,
    PortfolioOptimizationStrategy,
    AdaptiveStrategy
)
import matplotlib.pyplot as plt

# Enable the interactive mode in matplotlib
plt.ion()

cerebro = bt.Cerebro()

data = bt.feeds.YahooFinanceCSVData(
    dataname=f'samples/oracle.csv',
    fromdate=datetime.datetime(2000,1, 1),
    todate=datetime.datetime(2000,12,31)
)
cerebro.adddata(data)

cerebro.addstrategy(DualThrustStrategy)

cerebro.broker.setcash(10000)
cerebro.broker.setcommission(commission=0.005)

cerebro.run()

# Plot the result
figure = cerebro.plot()[0][0]

# Display the plot
plt.show(block=True)

