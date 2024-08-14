from ..data import UserDataEvent
from ..enums import ChannelType
from ..enums import EventType
from .handler import Handler


class OrderHandler(Handler):
    def __call__(self, event: UserDataEvent) -> None:  # type: ignore[override]
        if event.channel_type != ChannelType.ORDER:
            return

        super().__call__(event)


class OrderSnapshotHandler(OrderHandler):
    def __call__(self, event: UserDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.SNAPSHOT:
            return

        super().__call__(event)


class OrderUpdateHandler(OrderHandler):
    def __call__(self, event: UserDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.UPDATE:
            return

        super().__call__(event)
