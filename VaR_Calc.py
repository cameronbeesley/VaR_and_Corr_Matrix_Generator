import yfinance as yf

# Fetch EUR/USD data
ticker = "EURUSD=X"
data = yf.download(ticker, start="2021-01-01", end="2026-01-01")['Close']

# Calculate daily percentage change
returns = data.pct_change().dropna()

import numpy as np

confidence_level = 0.95
# Find the 5th percentile (the bottom 5% of days)
var_percentile = np.percentile(returns, (1 - confidence_level) * 100)

portfolio_value = 10_000_000  # £10 Million
var_amount = portfolio_value * var_percentile

print(f"95% 1-day VaR: £{abs(var_amount):,.2f}")

# create a histogram showing the distribution of returns
import matplotlib.pyplot as plt
plt.hist(returns, bins=100)
plt.show()

# ----------------------------------------- Fetch EUR/JPY ---------------------------------------------------
ticker = "EURJPY=X"
data = yf.download(ticker, start="2021-01-01", end="2026-01-01")['Close']

# Calculate daily percentage change
returns = data.pct_change().dropna()

confidence_level = 0.95
# Find the 5th percentile (the bottom 5% of days)
var_percentile = np.percentile(returns, (1 - confidence_level) * 100)

portfolio_value = 10_000_000  # £10 Million
var_amount = portfolio_value * var_percentile

print(f"95% 1-day VaR: £{abs(var_amount):,.2f}")

# create a histogram showing the distribution of returns
import matplotlib.pyplot as plt
plt.hist(returns, bins=100)
plt.show()
