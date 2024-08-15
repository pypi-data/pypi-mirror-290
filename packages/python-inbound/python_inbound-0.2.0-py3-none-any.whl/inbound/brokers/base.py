from abc import ABC, abstractmethod
from typing import Tuple, Type

from inbound.event import Event
from inbound.serializers import JSONSerializer, Serializer


class Broker(ABC):
    def __init__(self, url: str, serializer: Type[Serializer] = JSONSerializer):
        self._url = url
        self._serializer = serializer

    @abstractmethod
    async def connect(self) -> None:
        """
        Connect to the broker
        """
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """
        Close the connection to the broker
        """
        ...

    @abstractmethod
    async def subscribe(self, channel: str) -> None:
        """
        Subscribe to a specific channel

        :param channel: The name of the channel to subscribe to
        :type channel: str
        """
        ...

    @abstractmethod
    async def unsubscribe(self, channel: str) -> None:
        """
        Unsubscribe from a specific channel

        :param channel: The name of the channel to unsubscribe
        :type channel: str
        """
        ...

    @abstractmethod
    async def publish(self, channel: str, event: Event, **kwargs) -> None:
        """
        Publish an event to a given channel

        :param event: The Event to publish
        :type event: Event
        """
        ...

    @abstractmethod
    async def next(self) -> Tuple[str, Event]:
        """
        Get the next event from the broker
        """
        ...
