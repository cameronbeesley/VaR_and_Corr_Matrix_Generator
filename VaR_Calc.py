import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

currencies = ["USD", "GBP", "EUR", "JPY", "AUD", "CAD", "CNY", "CHF", "HKD"]
sCurrencies = ' '.join(currencies)

def calculateVaR(portfolioValue, originalCurrency, conversionCurrency, tradingDays):
    '''
    Given the porfolio value, original and conversion currency, this will calculate the VaR to a 95% confidence level
    Finally it will display a histogram of the returns
    '''
    ticker = f"{originalCurrency}{conversionCurrency}=X"
    data = yf.download(ticker, start="2021-01-01", end="2026-01-01")['Close']
    returns = data.pct_change().dropna()
    confindenceLevel = 0.95
    varPercentile = np.percentile(returns, (1 - confindenceLevel) * 100)
    varAmount = varPercentile * portfolioValue * np.sqrt(tradingDays)
    print(f"95% {tradingDays}-day VaR from {originalCurrency} to {conversionCurrency}: {abs(varAmount):,.2f}")

    # displaying the return history in a histogram
    plt.hist(returns, bins=100)
    plt.show()

    # calling monte carlo simulation
    monteCarlo(portfolioValue, returns, tradingDays)

    temp = input("\nPress enter to exit")

def monteCarlo(portfolioValue, returns, tradingDays):
    mu = float(returns.mean().iloc[0]) if hasattr(returns.mean(), 'iloc') else float(returns.mean())
    sigma = float(returns.std().iloc[0]) if hasattr(returns.std(), 'iloc') else float(returns.std())   
    T = tradingDays
    simulations = 10000

    df = 3
    dailyShocks = np.random.standard_t(df, size=(T, simulations)) * sigma + mu
    pricePaths = portfolioValue * (1 + dailyShocks).cumprod(axis=0)

    simDf = pd.DataFrame(pricePaths)
    plt.figure(figsize=(10,6))
    plt.plot(simDf.iloc[:, :100]) # Plot only first 100 paths so it's not too messy
    plt.title(f"Monte Carlo: 100 Possible Paths over {T} Days")
    plt.xlabel("Days")
    plt.ylabel("Portfolio Value")
    plt.show()

    finalValues = pricePaths[-1, :]
    confidenceLevel = 0.95
    lowerPercentile = np.percentile(finalValues, (1- confidenceLevel) * 100)
    print(f"Simulated VaR: {portfolioValue - lowerPercentile:,.2f}")

def getVaRInfo():
    '''
    Prompts the user for the information required to calculate the desired VaR
    Calls the calculate VaR function
    '''
    os.system('cls')
    # Prompting user for information to calculate VaR
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

    # getting the validating number of trading days
    valid = False
    while not valid:
        try: 
            tradingDays = int(input("How many trading days? "))
        except:
            valid = False
        else: 
            valid = True

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
    os.system('cls')
    print("Calculating VaR at 95 conversion interval...\n")
    calculateVaR(portfolioValue, originalCurrency, conversionCurrency, tradingDays)

def generateCorrMatrix(tickers):
    '''
    Generates and displays the correlation matrix for the selected assets
    '''
    # getting data and returns
    data = yf.download(tickers, start="2021-01-01", end="2026-01-01")['Close']
    returns = data.pct_change().dropna()

    # creating correlation matrix
    corr_matrix = returns.corr()

    # Displaying with seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Macro Assets Correlation Matrix')
    plt.show()

def getCMData():
    '''
    Gets the assets/tickers required for the correlation matrix
    Calls the function to generate the matrix
    '''
    os.system('cls')
    # getting and validating original currency
    originalCurrency = input(f"What currency are you converting from (e.g. {sCurrencies})? ")
    while originalCurrency not in currencies:
        print(f"{originalCurrency} is not a valid option - try again")
        originalCurrency = input(f"What currency are you converting from (e.g. {sCurrencies})? ")
    
    # getting and display the asset/ticker option
    os.system('cls')
    displayOptions, codeOptions = generateTickerOptions(originalCurrency)
    print("Asset Options:")
    print('\n'.join(displayOptions))

    # getting the user to pick their desired assets and validating
    choice = input("Select which assets you would like to include, seperated by ',' (e.g. 1,4,5 or ALL - for all options): ")
    valid = False

    # generating tickers list
    os.system('cls')
    if choice == "ALL":
        tickers = codeOptions
    else:
        tickers = []
        for c in choice.split(','):
            try:
                i = int(c) - 1
            except:
                print(f"{c} is an invalid - skipped")
            else:
                if 0 <= i < len(codeOptions):
                    if codeOptions[i]  not in tickers:
                        tickers.append(codeOptions[i])
                else:
                    print(f"{c} is an invalid option - skipped")

    # generating matrix if there are tickers
    if len(tickers) == 0:
        print("No valid tickers - try again")
        getCMData()
    else:
        print("Calculating Correlation Matrix...")
        generateCorrMatrix(tickers)

def generateTickerOptions(originalCurrency):
    '''
    Generates all the valid ticker options
    Returns a list of the options in a displayable format and a list of the option in the yfinance format
    '''
    # other assets
    displayOptions = ["1 - Gold Futures", "2 - S&P 500", "3 - 10-Year Treasury Bond Yeild", "4 - Bitcoin", "5 - Apple"]
    codeOptions = ["GC=F", "^GSPC", "^TNX", f"BTC-{originalCurrency}", "AAPL"]

    # currencies
    i = len(codeOptions) + 1
    for currency in currencies:
        if currency != originalCurrency:
            displayOptions.append(f"{i}: {currency}")
            codeOptions.append(f"{originalCurrency}{currency}=X")
            i += 1
    return displayOptions, codeOptions

def main():
    choice = ''
    while choice != '3':
        os.system('cls')
        choice = ''
        while choice not in ['1', '2', '3']:
            choice = input("What would you like to calculate?\n1 - VaR\n2 - Correlation Matrix\n3 - Quit\nEnter your choice: ")
        if choice == '1':
            getVaRInfo()
        elif choice == '2':
            getCMData()
    os.system('cls')

if __name__ == "__main__":
    main()

# Monte Carlo Simulator

# ticker = f"EURUSD=X"
# data = yf.download(ticker, start="2021-01-01", end="2026-01-01")['Close']
# returns = data.pct_change().dropna()

# # 1. Setup Parameters from your existing 'returns' data
# mu = returns.mean()        # Average daily return (Drift)
# sigma = returns.std()     # Daily volatility (Shock)
# S0 = 100000                          # Starting investment (£100k)
# T = 252                              # Time horizon (1 trading year)
# simulations = 10000                  # Number of "Future Paths"

# # 2. Run the Simulation
# # We generate a grid of random numbers (Days x Simulations)
# daily_shocks = np.random.normal(mu, sigma, (T, simulations))

# # Calculate price paths: We start at S0 and compound the random returns
# # Formula: Price_t = Price_{t-1} * (1 + random_return)
# price_paths = S0 * (1 + daily_shocks).cumprod(axis=0)

# # 3. Convert to a DataFrame for easy plotting
# sim_df = pd.DataFrame(price_paths)

# plt.figure(figsize=(10,6))
# plt.plot(sim_df.iloc[:, :100]) # Plot only first 100 paths so it's not too messy
# plt.title(f"Monte Carlo: 100 Possible Paths for BTC-USD over {T} Days")
# plt.xlabel("Days")
# plt.ylabel("Portfolio Value")
# plt.show()

# # Get the final value of each of the 10,000 paths
# final_values = price_paths[-1, :]

# # Find the 5th percentile (the bottom 5% of outcomes)
# simulated_var = np.percentile(final_values, 5)
# print(f"Potential Loss (VaR): {S0 - simulated_var:,.2f}")
