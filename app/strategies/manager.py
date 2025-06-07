from typing import List
from app.strategies.base import BaseStrategy

class StrategyManager:
    def __init__(self):
        self.strategies: List[BaseStrategy] = []

    def register(self, strategy: BaseStrategy):
        self.strategies.append(strategy)

    def initialize_all(self, ohlc: dict):
        for strategy in self.strategies:
            strategy.initialize(ohlc)

    def process_tick(self, tick: dict):
        for strategy in self.strategies:
            strategy.on_tick(tick)
