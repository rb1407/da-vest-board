import pandas as pd, os, time
year = time.localtime().tm_year
month = time.localtime().tm_mon

# Create directories to store clean returns
for i in ['1y', '3y']:
    os.makedirs(f"final/{i}/{month-1}_{year}", exist_ok = True)

"""
Drop out-of-range returns
(Range = [Q1 - 1.5IQR, Q3 + 1.5IQR])
"""
def drop_outliers(returns):
    q1 = returns['Return'].quantile(0.25)
    q3 = returns['Return'].quantile(0.75)
    iqr = q3 - q1
    returns = returns[(returns['Return'] >= q1 - 1.5*iqr) & (returns['Return'] <= q3 + 1.5*iqr)]
    return returns

for i in ['1y', '3y']:
    files = os.listdir(f"returns/{i}/{month-1}_{year}")
    files.remove("markets.csv")
    for f in files:
       returns = pd.read_csv(f"returns/{i}/{month-1}_{year}/{f}")
       returns = drop_outliers(returns).reset_index()
       returns['Rank'] = returns.index + 1 # Rank assets by risk-adjusted return
       
       # Order, format and save final version
       if 'Volatility' in returns.columns:
           returns = returns[['Rank', 'Name', 'Ticker', 'Return', 'Risk', 'Volatility', 'Follows Market Direction ?']]
       
       else:
           returns = returns[['Rank', 'Name', 'Ticker', 'Return', 'Risk']]
           
        
       returns = returns.rename(columns = {'Return' : 'Return (%)'})
       returns.to_csv(f"final/{i}/{month-1}_{year}/{f}", index = False)
