import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns
from datetime import date
from scipy.stats import norm

def moex_hist_plt(x, s=None, e=None, bins=50, log=True):
  
  if isinstance(x, str):
    x = [x]
  
  dfs = []
  
  for ticker in x:
    
    url = (
      f"https://iss.moex.com/iss/engines/stock/"
      f"markets/shares/securities/{ticker}/candles.json"
      )
    
    if s is None:
      s = "2007-01-01"  
      
    if e is None:
      e = date.today().isoformat()
      
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
      returns = x[column]
      mu, std = norm.fit(returns)
  
      plt.figure()
      plt.hist(
        returns, 
        bins=bins, 
        density=True, 
        edgecolor="black", 
        alpha=0.7
        )
  
      grid = np.linspace(returns.min(), returns.max(), 200)
      plt.plot(
        grid, 
        norm.pdf(grid, mu, std), 
        "r", 
        linewidth=2,
        label=f"Normal fit: μ={mu:.2f}, σ={std:.2f}"
        )
  
      plt.title(column)
      plt.xlabel("Returns, %")
      plt.ylabel("Density")
      plt.legend()
      plt.grid(True, linestyle=":", color="grey")
      plt.show()

moex_hist_plt(
  ["SBER", "GAZP", "PHOR", "PLZL", "GMKN"]
  ) # Display
