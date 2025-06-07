from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
from app.pubsub.tick_publisher import TickPublisher

class AngelOneWebSocket:
    def __init__(self, auth_token, api_key, client_code, feed_token):
        self.sws = SmartWebSocketV2(auth_token, api_key, client_code, feed_token)

        # Assigning callback methods
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close

    def on_open(self, wsapp):
        logger.info("WebSocket opened.")
        token_list = [
            {
                "exchangeType": 1,  # 1 = NSE, 2 = BSE
                "tokens": ["3045"]  # SBIN-EQ (symbol token)
            }
        ]
        correlation_id = "tick-stream"
        mode = 1  # 1 = LTP, 2 = Quote, 3 = SnapQuote, 4 = Full
        self.sws.subscribe(correlation_id, mode, token_list)


    def on_data(self, wsapp, message):
        # You may want to standardize this tick structure
        tick_data = {
            "symbol": message.get("token"),
            "ltp": message.get("last_traded_price") / 100  # Assuming price in paise
        }
        TickPublisher().publish(tick_data)


    def on_error(self, wsapp, error):
        logger.error(f"WebSocket error: {error}")

    def on_close(self, wsapp):
        logger.info("WebSocket closed")

    def connect(self):
        self.sws.connect()

    def close_connection(self):
        self.sws.close_connection()
