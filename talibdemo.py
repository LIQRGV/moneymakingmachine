import numpy as np
import pandas as pd
import talib
import datetime as dt

data = pd.read_csv("stock/BBRI.JK.csv", index_col=0, parse_dates=True).convert_objects(convert_numeric=True).dropna().tail(100)

# note that all ndarrays must be the same length!
# inputs = {
#     'open': np.random.random(100),
#     'high': np.random.random(100),
#     'low': np.random.random(100),
#     'close': np.random.random(100),
#     'volume': np.random.random(100)
# }

prices = {
    'open': np.array(data['Open'].values),
    'high': np.array(data['High'].values),
    'low': np.array(data['Low'].values),
    'close': np.array(data['Close'].values),
    'volume': np.array(data['Volume'].values)
}

# print(inputs)

# print(talib.ATR(prices['high'], prices['low'], prices['close'],timeperiod=14)[-1])

date = dt.datetime.now()

upper, middle, lower = talib.BBANDS(
        prices['close'],
        timeperiod=10,
        # number of non-biased standard deviations from the mean
        nbdevup=2,
        nbdevdn=2,
        # Moving average type: simple moving average here
        matype=0)

# print(upper[-1])

integer = talib.CDLHAMMER(prices['open'], prices['high'], prices['low'], prices['close'])
print(integer[-1])


print(talib.ADX(prices['high'], prices['low'], prices['close'])[-1])
print(talib.PLUS_DI(prices['high'], prices['low'], prices['close'])[-1])
print(talib.MINUS_DI (prices['high'], prices['low'], prices['close'])[-1])