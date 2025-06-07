from app.services.brokers.angelone import AngelOneBroker
from app.services.brokers.angelone_ws import AngelOneWebSocket
from app.pubsub.tick_publisher import TickPublisher
from app.strategies.camarilla import CamarillaStrategy
from app.strategies.manager import StrategyManager
from app.config import settings
from logzero import logger

# 🔁 For mock data
from app.services.mock_tick_generator import MockTickGenerator

def main():
    use_mock_data = True  # 🔁 Set this to False to use live WebSocket
    symbol = "NSE:RELIANCE-EQ"


    if use_mock_data:
        logger.info("Using mock tick data...")
        dummy_ohlc = {
            "high": 820,
            "low": 810,
            "close": 815
        }
        camarilla = CamarillaStrategy(symbol=symbol)
        camarilla.initialize(dummy_ohlc)
        strategy_manager = StrategyManager(strategies=[camarilla])
        TickPublisher.subscribe(strategy_manager.on_tick)

        mock_generator = MockTickGenerator()
        mock_generator.start()
    else:
        broker = AngelOneBroker()
        session_data = broker.login()

        if not session_data:
            logger.error("Login failed. Exiting...")
            return

        logger.info("Login successful")

        camarilla = CamarillaStrategy(symbol=symbol)
        dummy_ohlc = {
            "high": 820,
            "low": 810,
            "close": 815
        }
        camarilla.initialize(dummy_ohlc)
        strategy_manager = StrategyManager(strategies=[camarilla])
        TickPublisher.subscribe(strategy_manager.on_tick)

        ws = AngelOneWebSocket(
            auth_token=session_data["auth_token"],
            api_key=settings.SMARTAPI_API_KEY,
            client_code=settings.SMARTAPI_CLIENT_CODE,
            feed_token=session_data["feed_token"]
        )
        ws.connect()

if __name__ == "__main__":
    main()
