from app.services.brokers.angelone import AngelOneBroker
from app.services.brokers.angelone_ws import AngelOneWebSocket
from app.pubsub.tick_publisher import TickPublisher

from app.strategies.camarilla import CamarillaStrategy
from app.strategies.manager import StrategyManager

from app.config import settings
from logzero import logger


def main():
    broker = AngelOneBroker()
    session_data = broker.login()

    if not session_data:
        logger.error("Login failed. Exiting...")
        return

    logger.info("Login successful")

    # Step 1: Initialize the strategy
    camarilla = CamarillaStrategy()

    # Use dummy OHLC data for now
    dummy_ohlc = {
        "high": 820,
        "low": 810,
        "close": 815
    }
    camarilla.initialize(dummy_ohlc)

    # Step 2: Register strategy with StrategyManager
    strategy_manager = StrategyManager(strategies=[camarilla])
    TickPublisher.subscribe(strategy_manager)

    # Step 3: Start WebSocket
    ws = AngelOneWebSocket(
        auth_token=session_data["auth_token"],
        api_key=settings.SMARTAPI_API_KEY,
        client_code=settings.SMARTAPI_CLIENT_CODE,
        feed_token=session_data["feed_token"]
    )
    ws.connect()


if __name__ == "__main__":
    main()
