import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

def moex_boxplot(x, s, e, main=None):
  
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
  
  dfs = pd.concat(dfs, axis=1)
  
  dfs = np.log(dfs / dfs.shift(1)).dropna()
     
  dfs.plot(kind="box")    
  plt.title(main)
  plt.xlabel("Data Source: MOEX")
  plt.ylabel("Returns")
  plt.grid(True, linestyle=":", color="grey")
  plt.axhline(y=0, color='grey', linestyle='--')
  plt.show()
    
moex_boxplot(
  ["SBER", "GAZP", "PHOR", "PLZL", "GMKN"], 
  "2017-01-01", "2024-12-31",
  main = "Boxplot of Russian companies"
)
