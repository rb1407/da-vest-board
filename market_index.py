import pandas as pd, yfinance as yf, math, time, os
year = time.localtime().tm_year
month = time.localtime().tm_mon

# Make directories to store market returns by country
for i in ['1y', '3y']:
    os.makedirs(f"returns/{i}/{month-1}_{year}", exist_ok = True)
    os.makedirs(f"final/{i}/{month-1}_{year}", exist_ok = True)

"""
Calculates i-market returns, as observed in market index, by country
"""
def calc_market_returns(data, i):
    # Calculate monthly holding period returns
    lag = data.shift(1)
    data = data.iloc[1:, :]
    lag = lag.iloc[1:, :]
    returns = (data - lag)/lag
    
    # Drop any rows and columns with no data at all
    returns = returns.dropna(how = "all", axis = 1)
    tickers_new = [col for col in returns.columns]
    returns = returns.dropna(how = "all", axis = 0)
    
    # Calculate Sharpe ratios by country
    return_stats = returns[tickers_new].agg(['mean', 'std']).T
    return_stats['sharpe'] = return_stats['mean']/return_stats['std']
    
    return_stats['Return'] = ((1 + return_stats['mean'])**12 - 1)*100 # Annualized return
    return_stats['Return'] = return_stats['Return'].round(2)
    return_stats['Risk'] = return_stats['std']*math.sqrt(12) # Annualized risk
    return_stats['Risk'] = return_stats['Risk'].round(3)
    
    # Merge with driver directory, and sort in descending order by Sharpe ratio
    return_stats = return_stats.merge(indices, left_index = True, right_on = 'Market Index Ticker', how = 'outer')
    return_stats = return_stats.sort_values(by = 'sharpe', ascending = False).reset_index()
    
    # Rank countries with a Sharpe ratio
    no_na = return_stats.dropna(subset = "sharpe")
    no_na['Rank'] = no_na.index + 1
    return_stats['Rank'] = no_na['Rank']
    
    # Format, order and save dataset
    return_stats = return_stats.rename(columns = {'Return' : 'Return (%)'})
    return_stats = return_stats[['Rank', 'ISO Code', 'Country', 'Market Index Name', 'Market Index Ticker', 'mean', 'std', 'sharpe', 'Return (%)', 'Risk']]
    return_stats.to_csv(f'returns/{i}/{month-1}_{year}/markets.csv', index = False)
    return_stats = return_stats.drop(columns = ['mean', 'std', 'sharpe'])
    return_stats.to_csv(f"final/{i}/{month-1}_{year}/markets.csv", index = False)

indices = pd.read_excel("Markets_by_Country.xlsx", index_col = 0, header = 0)

list_indices = list(indices["Market Index Ticker"])

# Download data for market indices, and filter for end-of-month figures
data = yf.download(list_indices, period = '3y')
data = data['Close'].reset_index()
data['Month'] = data['Date'].dt.month
data['Lead_Month'] = data['Month'].shift(-1)
data = data[data['Month'] != data['Lead_Month']]
data = data.drop(['Month', 'Lead_Month'], axis = 1).set_index('Date')
data = data[:-1] # Drop figures for present date

calc_market_returns(data, "3y")
calc_market_returns(data[-12:], "1y")

