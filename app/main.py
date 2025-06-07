from app.services.brokers.angelone import AngelOneBroker
from app.services.brokers.angelone_ws import AngelOneWebSocket
from app.services.brokers.mock_ws import MockWebSocket  # ✅ Import Mock WebSocket

from app.pubsub.tick_publisher import TickPublisher
from app.strategies.camarilla import CamarillaStrategy
from app.strategies.manager import StrategyManager
from app.config import settings
from logzero import logger


def main():
    broker = AngelOneBroker()
    session_data = broker.login()

    if not session_data:
        logger.warning("Login failed. Falling back to mock data...")
        run_mock_data()
        return

    logger.info("Login successful")

    # Step 1: Initialize the strategy
    camarilla = CamarillaStrategy()
    dummy_ohlc = {
        "high": 820,
        "low": 810,
        "close": 815
    }
    camarilla.initialize(dummy_ohlc)

    # Step 2: Register strategy with StrategyManager
    strategy_manager = StrategyManager(strategies=[camarilla])
    TickPublisher.subscribe(strategy_manager)

    # Step 3: Try live WebSocket. On failure, fallback to mock.
    try:
        ws = AngelOneWebSocket(
            auth_token=session_data["auth_token"],
            api_key=settings.SMARTAPI_API_KEY,
            client_code=settings.SMARTAPI_CLIENT_CODE,
            feed_token=session_data["feed_token"]
        )
        ws.connect()
    except Exception as e:
        logger.error(f"WebSocket connection failed: {e}")
        run_mock_data()


def run_mock_data():
    """Run mock WebSocket tick stream"""
    from time import sleep
    from threading import Thread

    camarilla = CamarillaStrategy()
    dummy_ohlc = {
        "high": 820,
        "low": 810,
        "close": 815
    }
    camarilla.initialize(dummy_ohlc)
    strategy_manager = StrategyManager(strategies=[camarilla])
    TickPublisher.subscribe(strategy_manager)

    mock_ws = MockWebSocket()
    t = Thread(target=mock_ws.start_stream)
    t.start()
    while True:
        sleep(1)


if __name__ == "__main__":
    main()
