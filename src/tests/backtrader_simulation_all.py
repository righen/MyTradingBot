import backtrader as bt
import datetime
import yfinance as yf
import pandas as pd
from strategies import (
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
    # SentimentAnalysisStrategy,
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
    # SentimentBasedStrategy,
    AlgorithmicTradingStrategy,
    PortfolioOptimizationStrategy,
    AdaptiveStrategy
)

# Download historical data from Yahoo Finance
def get_data(ticker):
    df = yf.download(ticker, start='2010-01-01')
    return df

# Strategy analyzer
class StrategyAnalyzer(bt.Analyzer):
    def get_analysis(self):
        return self.strategy.broker.getvalue()

def run_strategy(strategy, data_feeds):
    cerebro = bt.Cerebro()
    for data_feed in data_feeds:
        cerebro.adddata(data_feed)
    cerebro.addstrategy(strategy)
    cerebro.addanalyzer(StrategyAnalyzer, _name="value")
    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission=0.005)
    result = cerebro.run()
    final_value = result[0].analyzers.value.get_analysis()
    return final_value

if __name__ == "__main__":
    strategies = [
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
        # SentimentAnalysisStrategy,
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
        # SentimentBasedStrategy,
        AlgorithmicTradingStrategy,
        PortfolioOptimizationStrategy,
        AdaptiveStrategy
    ]

    results = {}
    for strategy in strategies:
        strategy_name = strategy.__name__
        print(f"Running strategy: {strategy_name}")

        # Add two data feeds for Pair Trading strategy
        if strategy_name in ["PairTrading", "StatisticalArbitrage", "MergerArbitrageStrategy", "ConvertibleArbitrageStrategy"]:
            data_feed1 = bt.feeds.PandasData(dataname=get_data('AAPL'))
            data_feed2 = bt.feeds.PandasData(dataname=get_data('MSFT'))
            final_value = run_strategy(strategy, [data_feed1, data_feed2])
        else:
            data_feed = bt.feeds.PandasData(dataname=get_data('AAPL'))
            final_value = run_strategy(strategy, [data_feed])

        results[strategy_name] = final_value
        print(f"{strategy_name}: Final Portfolio Value = {final_value}")

    # Convert results to DataFrame for better visualization
    results_df = pd.DataFrame.from_dict(results, orient='index', columns=['Final Portfolio Value'])
    results_df.sort_values(by='Final Portfolio Value', ascending=False, inplace=True)
    print(results_df)

    # Save results to CSV
    results_df.to_csv('strategy_results.csv')
