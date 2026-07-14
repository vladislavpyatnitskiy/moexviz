import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

def moex_drawdown_plt(x, s, e):
  
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
  
  x[x > 0] = 0
  
  for column in x.columns:
        plt.figure()  # Create a new figure for each plot
        plt.plot(x[column])
        plt.title(f"{column} Drawdown")
        plt.grid(True, linestyle=":", color="grey")
        plt.axhline(y=0, color="black")
        plt.xlabel('Trading Days')
        plt.ylabel('Negative Return (%)')
        plt.show()
  
moex_drawdown_plt(
  ["SBER", "GAZP", "PHOR", "PLZL", "GMKN"], "2017-01-01", "2024-12-31"
  )
