# INVESTELITY

A finance project meant at making it easier for people to make investing decisions around the world, this GitHub repository uses data from YahooFinance to rank and list equities from around the world based on risk-adjusted return.
It comprises the following Python scripts :

1. ___market_index.py :___ To rank stock markets around the world, based on the respective performances of their market indices over the last 1 and 3 years, in terms of risk-adjusted return.
2. ___pull_tickers.py :___ To pull a list of tickers for every equity and US-based fund around the world, listed on YahooFinance. Takes around *15 minutes* to run.
3. ___pull_prices.py :___ To pull daily price data for the past 3 years for all tickers available from YahooFinance. Takes around *24 hours* to run.
4. ___clean_prices.py :____ To drop assets for which the API price call returned erroneous (e.g. negative) data. Takes around *30 minutes* to run.
5. ___asset_analysis.py :___ To calculate annualized return, risk and volatility for each equity and US-based fund (based on both 1-year and 3-year prices) using monthly holding period returns (HPRs), and subsequently rank them on the basis of risk-adjusted return. Takes around *10 minutes* to run.
7. ___clean_returns.py :___ To drop equities and US-based funds with outlier (unrealistic) returns.
8. ___create_viz.py :___ To create Tableau-ready datasets for visualization.

The package must be run in the above order to ensure an error-free and smooth experience. Scripts must not be run more than once a month. Running the package more than once a month will not produce updated results, as returns are calculated on a momthly basis. 


