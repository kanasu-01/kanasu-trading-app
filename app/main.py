from fastapi import FastAPI
from app.config import Settings
from app.services.brokers.angelone import AngelOneBroker
from app.pubsub.tick_publisher import TickSubscriber

app = FastAPI()
settings = Settings()
broker= AngelOneBroker()
session_data = broker.login()
print("login successful")
print("Session Data:", session_data)

from app.services.brokers.angelone_ws import AngelOneWebSocket

if session_data:
    ws = AngelOneWebSocket(
        auth_token=session_data["data"]["jwtToken"].split(" ")[1],
        api_key=settings.SMARTAPI_API_KEY,
        client_code=settings.SMARTAPI_CLIENT_CODE,
        feed_token=session_data["data"]["feedToken"]
    )
    ws.connect()
    print("WebSocket connection established")

@app.get("/")
async def read_root():
    return {"messgae": f"App is running with API key: {settings.smartapi_api_key}"}

from app.strategies.manager import StrategyManager
from app.strategies.camarilla import CamarillaStrategy

# 1. Setup
strategy_manager = StrategyManager()
camarilla = CamarillaStrategy()
strategy_manager.register(camarilla)

# 2. Initialize with daily OHLC (mock for now)
strategy_manager.initialize_all({
    "high": 525,
    "low": 510,
    "close": 515
})

# 3. In WebSocket on_tick
strategy_manager.process_tick({
    "ltp": 526,
    "token": "3045"
})
TickSubscriber().subscribe(camarilla)
