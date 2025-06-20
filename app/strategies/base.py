from abc import ABC, abstractmethod
from app.pubsub.tick_publisher import TickPublisher

class BaseStrategy(ABC, TickPublisher):
    ""
    def __init__(self, symbol: str):
        self.symbol = symbol
    
    @abstractmethod
    def on_tick(self, tick: dict):
        """Process each incoming tick."""
        pass

    @abstractmethod
    def initialize(self, ohlc: dict):
        """Initialize strategy with daily OHLC data."""
        pass
