# This strategy was taken from http://www.investopedia.com/articles/trading/08/atr.asp

# The idea is to use ATR to identify breakouts, if the price goes higher than
# the previous close + ATR, a price breakout has occurred. The position is closed when
# the price goes 1 ATR below the previous close.

# This algorithm uses ATR as a momentum strategy, but the same signal can be used for
# a reversion strategy, since ATR doesn't indicate the price direction.

from dateutil import parser
import talib
from quants import *
import numpy as np

from strategy import Strategy


class RSIStrategy(Strategy):

    def order_target_percent(self, stock, param):
        self.portfolio_positions[stock].amount = param

        curr_price = self.data.current(stock, 'Close')

        profit = curr_price - self.buy_price

        if not self.has_open_position and (param == 1.0):
            self.buy(curr_price)

        elif self.has_open_position and (param == 0.0):
            self.sell(curr_price)

    def rebalance(self, context, data):
        # Load historical data for the stocks
        prices = data.history(self.stock, ['Close'], 300)

        # Get the rsi of this stock.
        # rsi = talib.RSI(prices['Close'], timeperiod=14)[-1]
        rsi = talib.RSI(prices['Close'], timeperiod=2)[-1]

        ma200 = talib.SMA(prices['Close'], 200)[-1]

        current_position = self.portfolio_positions[self.stock].amount

        curr_price = self.data.current(self.stock, 'Close')

        # RSI is above 70 and we own shares, time to sell
        if rsi > 70 and current_position > 0:
            self.order_target_percent(self.stock, 0)

        # RSI is below 30 and we don't have any shares, time to buy
        elif rsi < 30  and curr_price > ma200 and current_position == 0:
            self.order_target_percent(self.stock, 1)
