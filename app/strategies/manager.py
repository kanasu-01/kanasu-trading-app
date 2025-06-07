from typing import List
from app.strategies.base import BaseStrategy
from app.pubsub.tick_publisher import TickPublisher
from logzero import logger

class StrategyManager(TickPublisher):
    def __init__(self,strategies:list):
        self.strategies =strategies

    def register(self, strategy: BaseStrategy):
        self.strategies.append(strategy)

    def initialize_all(self, ohlc: dict):
        for strategy in self.strategies:
            strategy.initialize(ohlc)

    def process_tick(self, tick: dict):
        for strategy in self.strategies:
            strategy.on_tick(tick)
    def on_tick(self, tick: dict):
        logger.debug(f"[StrategyManager] Tick received: {tick}")
        for strategy in self.strategies:
            strategy.on_tick(tick)
