import pandas as pd, os, time
year = time.localtime().tm_year
month = time.localtime().tm_mon

# Make directory for latest visualizations
os.makedirs(f"viz/{month-1}_{year}", exist_ok = True)


indices = pd.read_excel("Markets_by_Country.xlsx", index_col = 0, header = 0)
for i in ['1y', '3y']:
    files = os.listdir(f"final/{i}/{month-1}_{year}")
    files.remove("markets.csv")
    files.remove("usf.csv")
    viz = pd.DataFrame()
    
    # Concatenate final-versions, with country name attached
    for f in files:
       r = pd.read_csv(f"final/{i}/{month-1}_{year}/{f}")
       r['Country'] = indices.loc[f.split(".")[0], 'Country']
       viz = pd.concat([viz, r])
    viz.to_csv(f"viz/{month-1}_{year}/{i}.csv", index = False)
