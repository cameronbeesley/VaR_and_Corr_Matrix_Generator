import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# # Fetch EUR/USD data
# ticker_USD = "EURUSD=X"
# data_USD = yf.download(ticker_USD, start="2021-01-01", end="2026-01-01")['Close']

# # Calculate daily percentage change
# returns_USD = data_USD.pct_change().dropna()

# confidence_level_USD = 0.95
# # Find the 5th percentile (the bottom 5% of days)
# var_percentile_USD = np.percentile(returns_USD, (1 - confidence_level_USD) * 100)

# portfolio_value_USD = 10_000_000  # £10 Million
# var_amount_USD = portfolio_value_USD * var_percentile_USD

# print(f"95% 1-day VaR: £{abs(var_amount_USD):,.2f}")

# # create a histogram showing the distribution of returns
# plt.hist(returns_USD, bins=100)
# plt.show()

# # ----------------------------------------- Fetch EUR/JPY ---------------------------------------------------
# ticker_JPY = "EURJPY=X"
# data_JPY = yf.download(ticker_JPY, start="2021-01-01", end="2026-01-01")['Close']

# # Calculate daily percentage change
# returns_JPY = data_JPY.pct_change().dropna()

# confidence_level_JPY = 0.95
# # Find the 5th percentile (the bottom 5% of days)
# var_percentile_JPY = np.percentile(returns_JPY, (1 - confidence_level_JPY) * 100)

# portfolio_value_JPY = 10_000_000  # £10 Million
# var_amount_JPY = portfolio_value_JPY * var_percentile_JPY

# print(f"95% 1-day VaR: £{abs(var_amount_JPY):,.2f}")

# # create a histogram showing the distribution of returns
# import matplotlib.pyplot as plt
# plt.hist(returns_JPY, bins=100)
# plt.show()

# #----------------------------------------- Creating a correlation martix---------------------------------------------------



# # Getting data and returns
# tickers_MATRIX = ["EURUSD=X", "EURJPY=X", "GBPUSD=X", "GC=F", "^GSPC", "^TNX"] 
# data_MATRIX = yf.download(tickers_MATRIX, start="2021-01-01", end="2026-01-01")['Close']
# returns_MATRIX = data_MATRIX.pct_change().dropna()

# # creating correlation matrix
# corr_matrix = returns_MATRIX.corr()
# print(corr_matrix)

# # Displaying with seaborn
# plt.figure(figsize=(10, 8))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
# plt.title('Macro Assets Correlation Matrix')
# plt.show()

def calculateVaR(portfolioValue, originalCurrency, conversionCurrency):
    '''
    Given the porfolio value, original and conversion currency, this will calculate the VaR to a 95% confidence level
    Finally it will display a histogram of the returns
    '''
    ticker = f"{originalCurrency}{conversionCurrency}=X"
    data = yf.download(ticker, start="2021-01-01", end="2026-01-01")['Close']
    returns = data.pct_change().dropna()
    confindenceLevel = 0.95
    varPercentile = np.percentile(returns, (1 - confindenceLevel) * 100)
    varAmount = varPercentile * portfolioValue
    print(f"95% 1-day VaR from {originalCurrency} to {conversionCurrency}: £{abs(varAmount):,.2f}")

    # displaying the return history in a histogram
    plt.hist(returns, bins=100)
    plt.show()

def getVaRInfo():
    '''
    Prompts the user for the information required to calculate the desired VaR
    Calls the calculate VaR function
    '''
    # Prompting user for information to calculate VaR
    currencies = ["USD", "GBP", "EUR", "JPY"]
    sCurrencies = ' '.join(currencies)

    # getting and validating original currency
    originalCurrency = input(f"What currency are you converting from (e.g. {sCurrencies})? ")
    while originalCurrency not in currencies:
        print(f"{originalCurrency} is not a valid option - try again")
        originalCurrency = input(f"What currency are you converting from (e.g. {sCurrencies})? ")

    # getting and validating conversion currency
    conversionCurrency = input(f"What currency are you converting to (e.g {sCurrencies})? ")
    while conversionCurrency not in currencies or conversionCurrency == originalCurrency:
        print(f"{originalCurrency} is not a valid option - try again")
        conversionCurrency = input(f"What currency are you converting to (e.g {sCurrencies})? ")

    # getting and validating portfolio value
    valid = False
    while not valid:
        try: 
            portfolioValue = int(input("What is the value of your portfolio? "))
        except:
            valid = False
        else: 
            valid = True
            
    # calculating VaR
    print("\nCalculating VaR at 95 conversion interval...\n")
    calculateVaR(portfolioValue, originalCurrency, conversionCurrency)

def main():
    getVaRInfo()

if __name__ == "__main__":
    main()


