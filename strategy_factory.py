# Create based on class name:
from moving_average import MovingAverageStrategy
from rsi_strategy import RSIStrategy


class StrategyFactory:
    def factory(type, symbol):
        if type == "RSI": return RSIStrategy(symbol)
        if type == "MOV": return MovingAverageStrategy(symbol)
        assert 0, "Bad strategy creation: " + type

    factory = staticmethod(factory)