from logzero import logger
from app.strategies.base import BaseStrategy

class CamarillaStrategy(BaseStrategy):
    def __init__(self, symbol: str):
        super().__init__(symbol)
        self.levels = None

    def initialize(self, ohlc: dict):
        high = ohlc['high']
        low = ohlc['low']
        close = ohlc['close']
        diff = high - low

        self.levels = {
            "R4": close + (diff * 1.1 / 2),
            "R3": close + (diff * 1.1 / 4),
            "R2": close + (diff * 1.1 / 6),
            "R1": close + (diff * 1.1 / 12),
            "S1": close - (diff * 1.1 / 12),
            "S2": close - (diff * 1.1 / 6),
            "S3": close - (diff * 1.1 / 4),
            "S4": close - (diff * 1.1 / 2),
        }
        logger.info(f"[{self.symbol}] Camarilla levels initialized: {self.levels}")

    def on_tick(self, tick: dict):
        if tick.get("token") != self.symbol:
            return  # Skip ticks not for this strategy's symbol

        if not self.levels:
            logger.warning(f"[{self.symbol}] Camarilla not initialized with OHLC")
            return

        ltp = tick.get("last_traded_price", 0) / 100  # Price in rupees

        if ltp > self.levels["R3"]:
            logger.info(f"[{self.symbol}] 🔼 Camarilla Buy Signal — LTP: ₹{ltp}")
        elif ltp < self.levels["S3"]:
            logger.info(f"[{self.symbol}] 🔽 Camarilla Sell Signal — LTP: ₹{ltp}")
