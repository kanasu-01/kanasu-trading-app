from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()
class Settings(BaseSettings):
    SMARTAPI_API_KEY: str
    SMARTAPI_CLIENT_CODE: str
    SMARTAPI_PIN:str
    SMARTAPI_TOTP_SECRET:str
    
    
    
    class Config:
        env_file = ".env"