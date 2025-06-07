import time
import random

class SyntheticTickGenerator:
    def __init__(self, instrument_token=12345, base_price=150, base_volume=10000):
        self.tk = instrument_token
        self.base_price = base_price
        self.last_price = base_price
        self.last_qty = 0
        self.total_volume = base_volume
        self.open_price = base_price - 1
        self.high_price = base_price + 1
        self.low_price = base_price - 1
        self.close_price = base_price - 0.5

    def get_next_tick(self):
        delta = random.uniform(-0.2, 0.2)
        self.last_price = max(0, self.last_price + delta)

        self.last_qty = random.randint(1, 20)
        self.total_volume += self.last_qty

        self.high_price = max(self.high_price, self.last_price)
        self.low_price = min(self.low_price, self.last_price)

        best_bid = round(self.last_price - random.uniform(0.05, 0.15), 2)
        best_ask = round(self.last_price + random.uniform(0.05, 0.15), 2)

        bid_qty = random.randint(50, 150)
        ask_qty = random.randint(50, 150)

        ts = int(time.time() * 1000)  # epoch milliseconds

        tick = {
            "t": "tx",
            "tk": self.tk,
            "ltp": round(self.last_price, 2),
            "ltq": self.last_qty,
            "v": self.total_volume,
            "o": round(self.open_price, 2),
            "h": round(self.high_price, 2),
            "l": round(self.low_price, 2),
            "c": round(self.close_price, 2),
            "a": best_ask,
            "b": best_bid,
            "atq": ask_qty,
            "btq": bid_qty,
            "ts": ts
        }
        return tick
