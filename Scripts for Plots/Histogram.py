import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns

def moex_hist_plt(x, s=None, e=None, bins=50, log=True):
  
  if isinstance(x, str):
    x = [x]
  
  dfs = []
  
  for ticker in x:
    
    url = (
      f"https://iss.moex.com/iss/engines/stock/"
      f"markets/shares/securities/{ticker}/candles.json"
      )
      
    params = {
        "from": s,
        "till": e,
        "interval": 24
    }
    
    all_rows = []
    start = 0
    
    while True:
      
      params["start"] = start
      r = requests.get(url, params=params)
      data = r.json()
      
      columns = data["candles"]["columns"]
      rows = data["candles"]["data"]
      
      if not rows:
        break
      
      all_rows.extend(rows)
      start += len(rows)
    
    df = pd.DataFrame(all_rows, columns=columns)
    
    df["Date"] = pd.to_datetime(df["begin"]).dt.date
    
    df = df[["close", "Date"]].set_index("Date").rename(
      columns={"close": ticker})
      
    dfs.append(df)
  
  p = pd.concat(dfs, axis=1)
  
  x = np.log(p / p.shift(1)).dropna() * 100
  
  for column in x.columns:
        plt.figure()  # Create a new figure for each plot
        plt.hist(x[column], bins=bins, edgecolor='black', alpha = 0.7)
        plt.title(column)
        plt.xlabel('Returns')
        plt.ylabel('Frequency')
        plt.grid(True, linestyle=":", color="grey")
        plt.show()

moex_hist_plt(
  ["SBER", "GAZP", "PHOR", "PLZL", "GMKN"], "2010-01-01", "2024-12-31"
  ) # Display
