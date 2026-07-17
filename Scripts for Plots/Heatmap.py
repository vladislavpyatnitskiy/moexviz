import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def moex_heat_map(x, s=None, e=None, method="pearson"):
  
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
  
  if method == "pearson":
    M = x.corr(method='pearson')  # Pearson correlation
  
  else:
    M = x.corr(method='spearman') # Spearman correlation
  
  plt.figure(figsize=(10, 8)) # Create the heatmap
  sns.heatmap(M, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
  plt.title(f'Stock Returns Heatmap by {method}')
  plt.show() # Show
  
moex_heat_map(
  ["SBER", "GAZP", "PHOR", "PLZL", "GMKN"], "2017-01-01", "2024-12-31",
  method="spearman"
)
