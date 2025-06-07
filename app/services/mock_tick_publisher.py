import threading
import time
from app.services.mock_tick_generator import MockTickGenerator

class SyntheticMockTickPublisher:
    def __init__(self, tick_subscriber, interval=0.5):
        """
        tick_subscriber: object with method on_tick(tick_dict)
        interval: time in seconds between ticks
        """
        self.tick_subscriber = tick_subscriber
        self.interval = interval
        self.running = False
        self.tick_generator = MockTickGenerator()

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._publish_loop)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.running = False

    def _publish_loop(self):
        while self.running:
            tick = self.tick_generator.get_next_tick()
            self.tick_subscriber.on_tick(tick)
            time.sleep(self.interval)
