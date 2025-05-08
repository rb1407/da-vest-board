import pandas as pd, yfinance as yf, json, time, os
year = time.localtime().tm_year
month = time.localtime().tm_mon

indices = pd.read_excel("Markets_by_Country.xlsx", index_col = 0, header = 0)

"""
Finds intradayprice-bounds to divide market-wide ticker-queries into, when more than 9000 tickers listed
(Uses binary search)
"""
def find_bounds(filt, reg, a, b, func, cum_left):
    bounds = []
    while cum_left > 9000:
        query = func('and', [func('lt', ['intradayprice', b]), func('gte', ['intradayprice', a]), func('eq', [filt, reg])])
        t = yf.screen(query)['total']
        if t > 9000:
           b = a + ((b-a)/2)
    
        else:
           bounds.append(b)
           a = b
           b = 2*b
           cum_left -= t
    bounds.append(-1) # To indicate last bound
    return bounds

"""
Forms queries to pull ticker and name information by region and type of asset
"""
def parse_ticker_queries(filt, reg, func):
    tickers = {}
    if reg != 'NAS': # For funds
       tickers[indices.loc[reg, 'Market Index Ticker']] = indices.loc[reg, 'Market Index Name']
       
    else: # For equities
       tickers[indices.loc['us', 'Market Index Ticker']] = indices.loc['us', 'Market Index Name']

    if yf.screen(func('eq',[filt, reg]))['total'] <= 9000:
       tickers_full = pull_tickers(func('eq', [filt, reg]))
       tickers.update(tickers_full)                          
    
    else:
        tot = yf.screen(func('eq',[filt, reg]))['total']
        bounds = find_bounds(filt, reg, 0, 100, func, tot)
        a = 0 
        
        for b in bounds:
            if b != -1:
               query = func('and', [func('lt', ['intradayprice', b]), func('gte', ['intradayprice', a]), func('eq', [filt, reg])])
            
            else:
                query = func('and', [func('gte', ['intradayprice', a]), func('eq', [filt, reg])])
    
            tickers_temp = pull_tickers(query)
            tickers.update(tickers_temp)
            a = b
    return tickers

"""
Returns ticker symbols and name by query, read in 100 at a time
"""
def pull_tickers(query):
    tickers = {}
    q_count = yf.screen(query)['total']

    for j in range(0, int(q_count/100) + 1):
       if j != int(q_count/100):
          q = yf.screen(query, offset = j*100, size = 100)
                                                
       else:
          q = yf.screen(query, offset = j*100, size = q_count - j*100)
                                                                                        
       for k in q['quotes']: 
          if 'longName' in k.keys():
            tickers[k['symbol']] = k['longName']
            
          elif 'shortName' in k.keys():
            tickers[k['symbol']] = k['shortName']
        
          else:
            tickers[k['symbol']] = ""
            
    return tickers

"""
Writes out tickers in JSON format
"""
def write_tickers(filename, tickers):
    with open(filename, 'w') as file:
        json.dump(tickers, file)

# Make directory to store tickers
os.makedirs(f"tickers/{month-1}_{year}", exist_ok = True)
for i in indices.index:
    write_tickers(f"tickers/{month-1}_{year}/{i}.json", parse_ticker_queries('region', i, yf.EquityQuery))

write_tickers(f"tickers/{month-1}_{year}/usf.json", parse_ticker_queries('exchange', 'NAS', yf.FundQuery))
