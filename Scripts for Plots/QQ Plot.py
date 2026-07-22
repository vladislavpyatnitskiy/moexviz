import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import probplot
import pandas as pd
import requests

def moex_qq_plot(x, s=None, e=None, log=False):
  
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
  

  # Compute returns 
  if log:
    p = np.log(p / p.shift(1)).dropna()
  else:
    p = (p / p.shift(1) - 1).dropna() * 100

  for column in p.columns:
    fig, ax = plt.subplots()
    probplot(p[column], plot=ax)
    ax.get_lines()[1].set(color='red', linewidth=2)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(f"{column} Q-Q Plot")
    plt.tight_layout()
    plt.show()

moex_qq_plot(
  ["SBER", "GAZP", "PHOR", "PLZL", "GMKN"], "2017-01-01", "2024-12-31",
  log=True
  )
