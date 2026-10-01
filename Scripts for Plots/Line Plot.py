import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from datetime import date

def moex_line_plt(x, s=None, e=None, board="TQBR"):
    if isinstance(x, str):
        x = [x]

    s = s or "2007-01-01"
    e = e or date.today().isoformat()

    series = []

    for ticker in x:
        url = (
            f"https://iss.moex.com/iss/engines/stock/markets/shares/"
            f"boards/{board}/securities/{ticker}/candles.json"
        )
        params = {"from": s, "till": e, "interval": 24}

        all_rows, start = [], 0
        while True:
            params["start"] = start
            r = requests.get(url, params=params)
            r.raise_for_status()
            candles = r.json()["candles"]
            columns, rows = candles["columns"], candles["data"]
            if not rows:
                break
            all_rows.extend(rows)
            start += len(rows)

        df = pd.DataFrame(all_rows, columns=columns)
        df["Date"] = pd.to_datetime(df["begin"]).dt.normalize()
        s_ = (df.drop_duplicates("Date")
                .set_index("Date")["close"]
                .rename(ticker))
        series.append(s_)

    dfs = pd.concat(series, axis=1).sort_index()

    plt.close("all")  # clear figures left over from earlier runs

    for column in dfs.columns:
        ser = dfs[column].dropna()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(ser.index, ser.values)
        ax.set_title(column)
        ax.grid(True, linestyle=":", color="grey")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price in Roubles")
        fig.tight_layout()
        plt.show()
        plt.close(fig)  # free the figure

moex_line_plt(["SBER", "GAZP", "PHOR", "PLZL", "GMKN"])
