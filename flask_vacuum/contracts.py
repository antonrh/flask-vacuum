import abc
from typing import Any, Callable, Optional, Type


class Event:
    pass


class EventDispatcher(abc.ABC):
    @abc.abstractmethod
    def subscribe(
        self,
        event_type: Type[Event],
        handler: Optional[Callable[[Event], None]] = None,
        sender: Optional[Any] = None,
    ) -> Any:
        """
        Register an event subscriber with the dispatcher.
        """

    @abc.abstractmethod
    def unsubscribe(
        self,
        event_type: Type[Event],
        handler: Optional[Callable[[Event], Any]] = None,
        sender: Optional[Any] = None,
    ) -> None:
        """
        Un-register an event subscriber from the dispatcher.
        """

    @abc.abstractmethod
    def dispatch(self, event: Event, sender: Optional[Any] = None) -> None:
        """
        Dispatch an event.
        """


class Scanner(abc.ABC):
    @abc.abstractmethod
    def scan(self) -> None:
        pass
