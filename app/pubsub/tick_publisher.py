from typing import List, Protocol


class TickSubscriber(Protocol):
    def on_tick(self, tick: dict):
        ...


class TickPublisher:
    _subscribers: List[TickSubscriber] = []

    @classmethod
    def subscribe(cls, subscriber: TickSubscriber):
        if subscriber not in cls._subscribers:
            cls._subscribers.append(subscriber)

    @classmethod
    def unsubscribe(cls, subscriber: TickSubscriber):
        if subscriber in cls._subscribers:
            cls._subscribers.remove(subscriber)

    @classmethod
    def publish(cls, tick: dict):
        for subscriber in cls._subscribers:
            subscriber.on_tick(tick)
