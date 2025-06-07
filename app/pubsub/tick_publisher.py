import asyncio
import random
import datetime
from typing import Callable

class TickPublisher:
    def __init__(self):
        self.subscribers = []
        self.running = False

    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)

    async def start(self):
        self.running = True
        print("Mock TickPublisher started sending ticks...")
        while self.running:
            tick = self.generate_mock_tick()
            for callback in self.subscribers:
                callback(tick)
            await asyncio.sleep(1)  # emit one tick per second (adjust as needed)

    def stop(self):
        self.running = False
        print("Mock TickPublisher stopped.")

    def generate_mock_tick(self):
        # Generate a realistic mock tick in Angel One websocket structure:
        now = datetime.datetime.utcnow()
        epoch = int(now.timestamp() * 1000)  # milliseconds

        # Mock instrument token (e.g., NIFTY 50)
        instrument_token = 256265

        # Prices simulated around a base price
        base_price = 18000
        ltp = round(base_price + random.uniform(-10, 10), 2)  # last traded price
        open_price = round(base_price + random.uniform(-20, 20), 2)
        high_price = max(ltp, open_price) + random.uniform(0, 5)
        low_price = min(ltp, open_price) - random.uniform(0, 5)
        close_price = round(base_price + random.uniform(-15, 15), 2)

        tick_data = {
            "exchange": "NFO",
            "instrument_token": instrument_token,
            "last_trade_price": ltp,
            "last_trade_quantity": random.randint(1, 100),
            "last_trade_time": epoch,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": random.randint(1000, 10000),
            "buy_quantity": random.randint(100, 1000),
            "sell_quantity": random.randint(100, 1000),
            "average_trade_price": round(base_price, 2),
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
        }

        return tick_data
