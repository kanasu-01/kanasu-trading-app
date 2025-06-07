from abc import ABC, abstractmethod

class BaseBroker(ABC):
    @abstractmethod
    def login(self):
        pass
""" 
    @abstractmethod
    def fetch_live_data(self, symbol: str):
        pass
    
    @abstractmethod
    def place_order(self, order_data: dict):
        pass
        
"""