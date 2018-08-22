# Create based on class name:
from adx_strategy import ADXStrategy
from atr_strategy import ATRStrategy
from bollinger_strategy import BollingerStrategy
from double7_strategy import Double7Strategy
from macd_strategy import MACDStrategy
from moving_average import MovingAverageStrategy
from purnaye_strategy import PurnayeStrategy
from rsi_cum_strategy import RSICumStrategy
from rsi_holy_strategy import RSIHolyStrategy
from rsi_powerzone_strategy import RSIPowerZoneStrategy
from rsi_strategy import RSIStrategy
from stoch_strategy import StochStrategy
from wvf_strategy import WVFStrategy


class StrategyFactory:
    def factory(type, symbol):
        if type == "RSI": return RSIStrategy(symbol)
        if type == "MOV": return MovingAverageStrategy(symbol)
        assert 0, "Bad strategy creation: " + type

    factory = staticmethod(factory)