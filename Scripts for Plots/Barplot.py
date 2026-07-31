import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns

def moex_bar_plt(x, s=None, e=None, col="blue"): # Bar plot
    
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

  x = ((np.exp(np.sum(np.log(p / p.shift(1)).dropna())) - 1) * 100)
        
  x = pd.DataFrame(x)
        
  x.columns = ['Return']
  
  x = x.sort_values(by = 'Return')
    
  x.plot(kind='bar')
  plt.title('Performance of Companies (%)')
  plt.grid(True, linestyle=":", color="grey")
  plt.axhline(y=0, color="black")
  plt.show()
    
moex_bar_plt(
  x=["SBER", "GAZP", "PHOR", "PLZL", "GMKN"], s="2023-10-01"
  ) # Test
