from angelone import AngelOneBroker
from logzero import logger

def main():
    try:
        broker = AngelOneBroker()
        broker.login()  # Ensure login is successful
        symbol_token = "26009"  # Example token for testing
        exchange_type = 1  # Example exchange type (NSE)
        broker.fetch_live_data(symbol_token, exchange_type)
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    main()
