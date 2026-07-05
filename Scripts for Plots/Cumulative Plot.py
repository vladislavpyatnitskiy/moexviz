import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

def moex_cum_rets(x, s, e, title=None):
  
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
  
  p = (np.exp(np.cumsum(np.log(p / p.shift(1)).dropna())) - 1) * 100
   
  plt.figure(figsize=(10, 6))
     
  plt.plot(p, label=x)
  plt.title(title)
  plt.xlabel('Trading Days')
  plt.ylabel('Return (%)')
  plt.legend()
  plt.grid(True)
  plt.show()
  
moex_cum_rets(
  ["SBER", "GAZP", "PHOR", "PLZL", "GMKN"], "2017-01-01", "2024-12-31",
  title = "Performance of Russian Stocks"
)
