from traceback import print_exc
from typing import Any

from gevent import spawn

from itflex import metrics

from .common.dataclasses import dataclass
from .queues import BaseQueue


@dataclass
class Event:
    name: str
    payload: Any


class EventsQueue(BaseQueue):
    def run(self):
        for event in self._queue:
            if not event:
                continue
            if event.name not in self._listeners:
                continue

            for listener in self._listeners[event.name]:
                spawn(self._handle_event, listener, event)

    def publish(self, name, payload):
        event = Event(name=name, payload=payload)
        self._queue.put(event)

    def _handle_event(self, listener, event):
        try:
            listener(event.payload)
        except Exception as error:
            print_exc()
            metrics.capture_exception(error)
            for handler in self._error_handlers:
                handler(error, event)


class BaseEvents:
    def __init__(self, queue):
        self.queue = queue
        self.event_created = None
        self.event_updated = None
        self.event_deleted = None

    def created(self, payload):
        self.queue.publish(self.event_created, payload)

    def updated(self, payload):
        self.queue.publish(self.event_updated, payload)

    def deleted(self, payload):
        self.queue.publish(self.event_deleted, payload)

