import pandas as pd, time, os
year = time.localtime().tm_year
month = time.localtime().tm_mon

# Make directories for clean prices
for i in ['1y', '3y']:
    os.makedirs(f"prices_cleaned/{i}/{month-1}_{year}", exist_ok = True)

"""
Drop assets with any out-of-range prices
(Range = [Q1 - 1.5IQR, Q3 + 1.5IQR])
"""
def drop_outliers(prices):
    for i in prices.columns:
        q1 = prices[i].quantile(0.25)
        q3 = prices[i].quantile(0.75)
        iqr = q3 - q1
        if (prices[i] < q1 - 1.5*iqr).any() | (prices[i] > q3 + 1.5*iqr).any() == True:
            prices = prices.drop(i, axis = 1)
            
    return prices

indices = pd.read_excel("Markets_by_Country.xlsx", index_col = 0, header = 0)
looper = list(indices.index)
looper.append('usf')
for i in looper:
    for j in ['1y', '3y']:
       prices = pd.read_csv(f"prices/{j}/{month-1}_{year}/{i}.csv").set_index('Date')
       
       # Drop negative prices
       col = prices.columns[(prices < 0).any()] 
       prices = prices.drop(columns = col)
       
       prices = drop_outliers(prices)
       prices.to_csv(f"prices_cleaned/{j}/{month-1}_{year}/{i}.csv")
       