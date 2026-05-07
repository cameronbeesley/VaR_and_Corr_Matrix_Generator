import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Fetch EUR/USD data
ticker_USD = "EURUSD=X"
data_USD = yf.download(ticker_USD, start="2021-01-01", end="2026-01-01")['Close']

# Calculate daily percentage change
returns_USD = data_USD.pct_change().dropna()

confidence_level_USD = 0.95
# Find the 5th percentile (the bottom 5% of days)
var_percentile_USD = np.percentile(returns_USD, (1 - confidence_level_USD) * 100)

portfolio_value_USD = 10_000_000  # £10 Million
var_amount_USD = portfolio_value_USD * var_percentile_USD

print(f"95% 1-day VaR: £{abs(var_amount_USD):,.2f}")

# create a histogram showing the distribution of returns
plt.hist(returns_USD, bins=100)
plt.show()

# ----------------------------------------- Fetch EUR/JPY ---------------------------------------------------
ticker_JPY = "EURJPY=X"
data_JPY = yf.download(ticker_JPY, start="2021-01-01", end="2026-01-01")['Close']

# Calculate daily percentage change
returns_JPY = data_JPY.pct_change().dropna()

confidence_level_JPY = 0.95
# Find the 5th percentile (the bottom 5% of days)
var_percentile_JPY = np.percentile(returns_JPY, (1 - confidence_level_JPY) * 100)

portfolio_value_JPY = 10_000_000  # £10 Million
var_amount_JPY = portfolio_value_JPY * var_percentile_JPY

print(f"95% 1-day VaR: £{abs(var_amount_JPY):,.2f}")

# create a histogram showing the distribution of returns
import matplotlib.pyplot as plt
plt.hist(returns_JPY, bins=100)
plt.show()

#----------------------------------------- Creating a correlation martix---------------------------------------------------

import pandas as pd
import seaborn as sns

# Getting data and returns
tickers_MATRIX = ["EURUSD=X", "EURJPY=X"]
data_MATRIX = yf.download(tickers_MATRIX, start="2021-01-01", end="2026-01-01")['Close']
returns_MATRIX = data_MATRIX.pct_change().dropna()

# creating correlation matrix
corr_matrix = returns_MATRIX.corr()
print(corr_matrix)

# Displaying with seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Macro Assets Correlation Matrix')
plt.show()


