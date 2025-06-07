from .base import BaseBroker
from app.config import Settings
from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import pyotp
from logzero import logger

class AngelOneBroker(BaseBroker):
        def __init__(self):
                self.settings=Settings()
                self.client = SmartConnect(api_key=self.settings.SMARTAPI_API_KEY)
                print("SmartConnect client initialized")
                
        def login(self):
            try:
                totp= pyotp.TOTP(self.settings.SMARTAPI_TOTP_SECRET).now()
                print(f"TOTP generated: {totp}")
            except Exception as e:
                logger.error(f"Error generating TOTP: {e}")
                raise e
            
            data=self.client.generateSession(
                self.settings.SMARTAPI_CLIENT_CODE,
                self.settings.SMARTAPI_PIN,
                totp
            )
            
            if data['status'] is False:
                logger.error(f"Login failed: {data}")
                return data
            
            self.auth_token = data['data']['jwtToken']
            self.refresh_token = data['data']['refreshToken']
            self.feed_token = self.client.getfeedToken()
            logger.info("Login successful")
            return data
            """_summary_
            
        def fetch_live_data(self, symbol_token: str, exchange_type: int = 1):
            try:
                correlation_id = "abc123"
                mode = 1  # Mode for live data
                token_list = [
                    {
                        "exchangeType": exchange_type,
                        "tokens": [symbol_token]
                    }
                ]

                sws = SmartWebSocketV2(
                    self.auth_token,
                    self.settings.SMARTAPI_API_KEY,
                    self.settings.SMARTAPI_CLIENT_CODE,
                    self.feed_token
                )

                def on_data(wsapp, message):
                    logger.info(f"Live data
                    sws.close_connection()  # Close connection after receiving data

                def on_error(wsapp, error):
                    logger.error(f"WebSocket error: {error}")

                def on_close(wsapp):
                    logger.info("WebSocket connection closed")

                sws.on_data = on_data
                sws.on_error = on_error
                sws.on_close = on_close

                sws.connect()
                sws.subscribe(correlation_id, mode, token_list)
            except Exception as e:
                logger.error(f"Error fetching live data: {e}")
                raise e
                    
        def place_order(self):
            print("Placing order...")
            # Implement order placement logic here:


"""
