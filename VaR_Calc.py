import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

currencies = ["USD", "GBP", "EUR", "JPY", "AUD", "CAD", "CNY", "CHF", "HKD"]
sCurrencies = ' '.join(currencies)

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

    temp = input("\nPress enter to exit")

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
    calculateVaR(portfolioValue, originalCurrency, conversionCurrency)

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


