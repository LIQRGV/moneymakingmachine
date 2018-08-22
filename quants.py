import datetime as dt
import pandas as pd


class Transaction:
    def __init__(self, buy_price, sell_price, hold_period, profitloss, profitlosspercent):
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.holding_period = hold_period
        self.profitloss = profitloss
        self.profitlosspercent = profitlosspercent

class Candle:
    def __init__(self, date, h, l, o, c):
        self.date = date
        self.high = h
        self.low = l
        self.open = o
        self.close = c


class Position:
    def __init__(self):
        self.amount = 0


class StockData:
    def __init__(self, symbols):
        self.symbols = symbols
        self.current_price = {}

        # need to create single price
        self.current_price2 = {}

        d = {}

        for i, stock in enumerate(symbols):
            self.current_price[stock] = 0.0
            d[stock] = pd.read_csv("stock/" + stock + '.JK.csv', index_col=0).convert_objects(convert_numeric=True).head(1)['Adj Close']

        self.prices = pd.DataFrame(d).dropna()

        self.prices2 = {}
        self.current_price2 = {}
        for i, stock in enumerate(symbols):
            self.prices2[stock] = pd.read_csv("stock/" + stock + '.JK.csv', index_col=0).convert_objects(convert_numeric=True).head(1)
            curr_price = self.prices2[stock].iloc[[0]]
            self.current_price2[stock] = Candle(curr_price.index[0], curr_price.High[0], curr_price.Low[0],
                                    curr_price.Open[0], curr_price.Close[0])

    def history1(self, length, period):
        return self.prices.tail(length)

    def history(self, stock, cols, length):
        return self.prices2[stock][cols].tail(length)

    def add(self, candles):

        for i, stock in enumerate(self.symbols):
            self.current_price[stock] = candles[stock].close

        row = []

        for i, stock in enumerate(self.symbols):
            row.append(candles[stock].close)

        first_key = list(candles.keys())[0]
        self.prices.loc[candles[first_key].date] = row

        row2 = []

        for i, stock in enumerate(self.symbols):
            row2.append(candles[stock].open)
            row2.append(candles[stock].high)
            row2.append(candles[stock].low)
            row2.append(candles[stock].close)
            row2.append(candles[stock].close)
            row2.append(0.0) # need to retrieve volume
            self.prices2[stock].loc[candles[first_key].date] = row2
            self.current_price2[stock] = candles[stock]
            row2 = []

    def current1(self, stock):
        return self.current_price[stock]

    def current(self, stock, col):

        if col == 'Close':
            return self.current_price2[stock].close
        elif col == 'Date':
            return self.current_price2[stock].date

        return self.current_price2[stock].close
