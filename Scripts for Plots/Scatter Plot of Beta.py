import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns

def moex_beta_plt(x, i="IMOEX", s=None, e=None):
    # Handle single-ticker string input BEFORE mutating
    if isinstance(x, str):
        x = [x]
    else:
        x = list(x)  # copy, so we don't mutate the caller's list
 
    tickers = x + [i]  # index goes last, no in-place mutation needed
 
    dfs = []
 
    for ticker in tickers:
        market = "index" if ticker == i else "shares"
        url = (
            f"https://iss.moex.com/iss/engines/stock/"
            f"markets/{market}/securities/{ticker}/candles.json"
        )
 
        params = {
            "from": s,
            "till": e,
            "interval": 24,
        }
 
        all_rows = []
        start = 0
 
        while True:
            params["start"] = start
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
 
            columns = data["candles"]["columns"]
            rows = data["candles"]["data"]
 
            if not rows:
                break
 
            all_rows.extend(rows)
            start += len(rows)
 
        if not all_rows:
            raise ValueError(
                f"No candle data returned for '{ticker}' (market='{market}'). "
                f"Check the ticker and date range."
            )
 
        df = pd.DataFrame(all_rows, columns=columns)
 
        df["Date"] = pd.to_datetime(df["begin"]).dt.date
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
 
        df = df[["close", "Date"]].set_index("Date").rename(
            columns={"close": ticker}
        )
        dfs.append(df)
 
    p = pd.concat(dfs, axis=1)
    p = np.log(p / p.shift(1)).dropna()  # log returns
 
    stocks = p[x]     # DataFrame with stock returns
    index = p[i]       # Series with index returns
 
    for column in stocks.columns:
        plt.figure()
        plt.scatter(x=index, y=stocks[column])
        sns.regplot(
          x=index, 
          y=stocks[column], 
          line_kws={"color": "red"}, 
          scatter=False
          )
        plt.title(f"{column} Beta Plot")
        plt.xlabel(f"{i} Return (%)")
        plt.ylabel(f"{column} Return (%)")
        plt.show()
 
moex_beta_plt(
    x=["SBER", "GAZP", "PHOR", "PLZL", "GMKN"],
    s="2010-01-01",
    e="2024-12-31",
)
