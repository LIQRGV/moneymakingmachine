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


class MovingAverageStrategy(Strategy):

    def order_target_percent(self, stock, param):
        self.portfolio_positions[stock].amount = param

        curr_price = self.data.current(stock, 'Close')

        profit = curr_price - self.buy_price

        if not self.has_open_position and (param == 1.0):
            self.buy(curr_price)

        elif self.has_open_position and (param == 0.0):
            self.sell(curr_price)

    def rebalance(self, context, data):
        hist = data.history(self.stock, ['Close'], 100)

        sma_50 = talib.SMA(hist['Close'], 30)[-1]
        sma_15 = talib.SMA(hist['Close'], 20)[-1]

        # print(sma_50)
        # print(sma_15)

        current_position = self.portfolio_positions[self.stock].amount

        # Close position for the stock when the MACD signal is negative and we own shares.
        if sma_15 > sma_50 and current_position == 0:
            self.order_target_percent(self.stock, 1.0)

        # Enter the position for the stock when the MACD signal is positive and
        # our portfolio shares are 0.
        elif sma_50 > sma_15 and current_position == 1.0:
            self.order_target_percent(self.stock, 0.0)
