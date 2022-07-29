import os
import pandas as pd
import yfinance as yf
from datetime import timedelta, datetime

symbols = [
    "EURUSD=X", "EURGBP=X", "EURAUD=X", "EURCAD=X",
    "EURCHF=X", "EURJPY=X", "EURNZD=X", "AUDCAD=X",
    "AUDCHF=X", "AUDJPY=X", "AUDNZD=X", "AUDUSD=X",
    "CADCHF=X", "CADJPY=X", "CHFJPY=X", "GBPAUD=X",
    "GBPCAD=X", "GBPCHF=X", "GBPJPY=X", "GBPNZD=X",
    "GBPUSD=X", "NZDCAD=X", "NZDCHF=X", "NZDJPY=X",
    "NZDUSD=X", "USDCAD=X", "USDCHF=X", "USDJPY=X"
]
START = '2019-01-01'
END = '2021-12-31'
for i in range(len(symbols)):
    try:
        symbol = symbols[i]
        print(symbol)
        data = yf.download(symbol, start=START, end=END)
        symbol = symbols[i][0:6]
        file = symbol + ".csv"
        data = data.dropna()
        data.to_csv('site/mysite/webapp/data/'+symbol+".csv")
    except:
        print("Unable to load data for {}".format(symbol))
# data.columns = pd.MultiIndex.from_tuples([i[::-1] for i in data.columns])
# print(data)
# save_location = ""
# for i in symbols:
#     TEMP = data[i].copy(deep=True)
#     TEMP = TEMP.dropna()
#     TEMP.to_csv("/" + i + ".csv")

