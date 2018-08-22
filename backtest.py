import pandas as pd
import numpy as np

from quants import Candle
from strategy_factory import StrategyFactory

def get_saham_list():
    fname = "sahamprofit.txt"
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content]

def run_backtest():
    symbols = ["BBCA", "BBRI", "UNTR", "BMRI", "TLKM"]

    metrics = []

    for i, symbol in enumerate(symbols):
        try:
            strategy = StrategyFactory.factory("RSI", symbol)
            prices = pd.read_csv("stock/" + symbol + '.JK.csv', index_col=0).convert_objects(convert_numeric=True)
            prices = prices[prices.index > "2007-01-01"]
            for i in range(1, len(prices)):
                current_price = prices.iloc[[i]]
                current_candle = Candle(current_price.index[0], current_price.High[0], current_price.Low[0],
                                        current_price.Open[0], current_price.Close[0])

                d = {symbol: current_candle}
                strategy.on_tick(d)
            metrics.append(strategy.calculate())
        except Exception as err:
            print("error : " + symbol + " " + format(err))

    for i, m in enumerate(sorted(metrics, key=lambda x: x.sharpe, reverse=True)):
        print(m.stock, m.sharpe, m.win_rate, m.profit, m.holding, m.notrans)

run_backtest()