import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def monte_carlo_simulation(df, num_simulations=1000, num_days=252):
    returns = df['4. close'].pct_change().dropna()
    last_price = df['4. close'].iloc[-1]

    simulation_df = pd.DataFrame()

    for x in range(num_simulations):
        daily_volatility = returns.std()
        price_series = [last_price]

        for _ in range(num_days):
            price = price_series[-1] * (1 + np.random.normal(0, daily_volatility))
            price_series.append(price)

        simulation_df[x] = price_series

    plt.figure(figsize=(10, 5))
    plt.plot(simulation_df)
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.title('Monte Carlo Simulation')
    plt.show()