from dataclasses import dataclass

import pytest
from flask import Flask

from flask_vacuum.events import Event, EventDispatcher
from flask_vacuum.exceptions import ImproperlyConfigured


@pytest.fixture()
def dispatcher(dummy_app: Flask):
    return EventDispatcher(app=dummy_app)


@dataclass
class DummyEvent(Event):
    pass


def test_event_subscribe_and_dispatch(dispatcher: EventDispatcher):

    event_dispatched = DummyEvent()
    event_subscribed = None

    def handler(event: DummyEvent):
        nonlocal event_subscribed
        event_subscribed = event

    dispatcher.subscribe(DummyEvent, handler)
    dispatcher.dispatch(event_dispatched)

    assert event_subscribed == event_dispatched


def test_event_subscribe_unsubscribe_and_dispatch(dispatcher: EventDispatcher):

    event_dispatched = DummyEvent()
    event_subscribed = None

    def handler(event: DummyEvent):
        nonlocal event_subscribed
        event_subscribed = event

    dispatcher.subscribe(DummyEvent, handler)
    dispatcher.unsubscribe(DummyEvent, handler)
    dispatcher.dispatch(event_dispatched)

    assert event_subscribed is None


def test_event_subscribe_with_decorator_and_dispatch(dispatcher: EventDispatcher):

    event_dispatched = DummyEvent()
    event_subscribed = None

    @dispatcher.subscribe(DummyEvent)
    def handler(event: DummyEvent):
        nonlocal event_subscribed
        event_subscribed = event

    dispatcher.dispatch(event_dispatched)

    assert event_subscribed == event_dispatched


def test_dispatch_invalid_type(dispatcher: EventDispatcher):

    with pytest.raises(TypeError):
        dispatcher.dispatch("invalid type")  # noqa


def test_subscribe_invalid_type(dispatcher: EventDispatcher):

    with pytest.raises(TypeError):
        dispatcher.subscribe("invalid type")(lambda _: _)  # noqa


def test_subscribe_no_app():

    dispatcher = EventDispatcher()

    with pytest.raises(ImproperlyConfigured) as exc_info:
        dispatcher.subscribe("invalid type")(lambda _: _)  # noqa

    assert str(exc_info.value) == "Event dispatcher is not initialized."


def test_unsubscribe_invalid_type(dispatcher: EventDispatcher):

    with pytest.raises(TypeError):
        dispatcher.unsubscribe("invalid type", lambda _: _)  # noqa
