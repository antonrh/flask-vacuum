import inspect
from typing import Any, Callable, Optional, Type

from blinker import Namespace
from flask import Flask, current_app, has_app_context
from injector import Module, inject, provider

from flask_vacuum import contracts
from flask_vacuum.contracts import Event
from flask_vacuum.exceptions import ImproperlyConfigured


class EventDispatcher(contracts.EventDispatcher):
    def __init__(self, app: Flask = None):
        self._signals = Namespace()
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app

    def subscribe(
        self,
        event_type: Type[Event],
        handler: Optional[Callable[[Event], None]] = None,
        sender: Optional[Any] = None,
    ) -> Any:

        sender = self._get_sender(sender)
        signal = self._signals.signal(event_type)

        if handler:

            def _receiver(_, event):
                return handler(event)

            setattr(_receiver, "__handler__", handler)
            signal.connect(_receiver, sender, weak=False)
            return

        def decorator(fn):

            if not self._ensure_event_type(event_type):
                raise TypeError("Invalid event type.")

            def wrapper(event):
                return fn(event)

            def receiver(_, event):
                return wrapper(event)

            receiver.__handler__ = fn

            signal.connect(receiver, sender, weak=False)

            return wrapper

        return decorator

    def unsubscribe(
        self,
        event_type: Type[Event],
        handler: Optional[Callable[[Event], Any]] = None,
        sender: Optional[Any] = None,
    ) -> None:

        sender = self._get_sender(sender)

        if not self._ensure_event_type(event_type):
            raise TypeError("Invalid event type.")

        signal = self._signals.signal(event_type)

        for receiver in signal.receivers_for(sender):
            receiver_handler = getattr(receiver, "__handler__", None)
            if receiver_handler == handler:
                signal.disconnect(receiver, sender)

    def dispatch(self, event: Event, sender: Optional[Any] = None) -> None:

        sender = self._get_sender(sender)

        if not isinstance(event, Event):
            raise TypeError("Invalid event type.")

        signal = self._signals.signal(event.__class__)
        signal.send(sender, event=event)

    def _get_sender(self, sender: Optional[Any] = None) -> Any:
        if sender:
            return sender
        if has_app_context():
            return current_app._get_current_object()  # noqa
        if not self.app:
            raise ImproperlyConfigured("Event dispatcher is not initialized.")
        return self.app

    @staticmethod
    def _ensure_event_type(event_type: Type[Event]):
        return inspect.isclass(event_type) and issubclass(event_type, Event)


class EventsModule(Module):
    @inject
    @provider
    def provide_event_dispatcher(self, app: Flask) -> contracts.EventDispatcher:
        return EventDispatcher(app)
