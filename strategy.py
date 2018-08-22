from quants import *
from dateutil import parser
import numpy as np


class Metrics:
    def __init__(self, s, wr, sh, p, h, nt):
        self.stock = s
        self.win_rate = wr
        self.sharpe = sh
        self.profit = p
        self.holding = h
        self.notrans = nt

class Strategy:
    def __init__(self, stock):
        self.stock = stock
        self.data = StockData([stock ])
        self.portfolio_positions = {stock: Position() }
        self.buy_price = 0
        self.buy_date = dt.datetime.now()
        self.has_open_position = False
        self.running_profit_percents = 0.0
        self.transactions = []

    def on_tick(self, candles):
        self.data.add(candles)
        self.rebalance(self.stock, self.data)

    def buy(self, curr_price):
        self.buy_price = curr_price
        self.has_open_position = True
        curr_date = self.data.current(self.stock, 'Date')
        self.buy_date = parser.parse(curr_date)
        # print(self.buy_date)

    def sell(self, curr_price):
        profit = curr_price - self.buy_price
        # print('profit', profit)

        percentage = profit / self.buy_price * 100

        # self.running_profit_percents += percentage

        sell_date = parser.parse(self.data.current(self.stock, 'Date'))
        holding_period = sell_date - self.buy_date

        trans = Transaction(self.buy_price, curr_price, holding_period, profit, percentage)
        self.transactions.append(trans)
        # self.print_details(trans)
        self.buy_price = 0
        self.has_open_position = False

    def print_details(self, trans):
        print('buy price', trans.buy_price)
        print('curr price', trans.sell_price)
        print('profit ', trans.profitloss)
        print('profit (%)', trans.profitlosspercent)
        print('PnL', self.running_profit_percents)
        print()

    def calculate(self):
        win_rate = 0
        profit_loss = 0
        profit_loss_rp = 0
        hold_period = 0
        returns = []

        for i, trans in enumerate(self.transactions):
            if trans.profitloss > 0:
                win_rate += 1

            returns.append(trans.profitlosspercent)
            profit_loss += trans.profitlosspercent
            profit_loss_rp += trans.profitloss
            hold_period += trans.holding_period.days

        no_trans = len(self.transactions)

        win_rate = round(win_rate / no_trans * 100)

        sharpe = self.annualised_sharpe(np.array(returns) - 0.05/252, 1)

        hold_period = round(hold_period / no_trans)

        print(self.stock)
        print('sharpe', sharpe)
        print('win rate (%)', win_rate)
        print('current price', self.data.current(self.stock, 'Close'))
        print('PnL Max (%)', np.max(returns))
        print('PnL Min (%)', np.min(returns))
        print('PnL ( Rp )', profit_loss_rp)
        print('# trans', no_trans)
        print('hold period', hold_period)
        print("")

        return Metrics(self.stock, win_rate, sharpe, profit_loss_rp, hold_period, no_trans)

    def annualised_sharpe(self, returns, N=252):
        """
        Calculate the annualised Sharpe ratio of a returns stream 
        based on a number of trading periods, N. N defaults to 252,
        which then assumes a stream of daily returns.

        The function assumes that the returns are the excess of 
        those compared to a benchmark.
        """
        return np.sqrt(N) * returns.mean() / returns.std()

    def order_target_percent(self, stock, param):
        self.portfolio_positions[stock].amount = param

        curr_price = self.data.current(stock, 'Close')

        # profit = curr_price - self.buy_price

        if not self.has_open_position and (param == 1.0):
            self.buy(curr_price)

        elif self.has_open_position and (param == 0.0):
            self.sell(curr_price)
