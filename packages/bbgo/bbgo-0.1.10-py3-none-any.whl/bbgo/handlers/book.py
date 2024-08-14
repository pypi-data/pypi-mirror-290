from ..data import MarketDataEvent
from ..enums import ChannelType
from ..enums import EventType
from .handler import Handler


class BookHandler(Handler):
    def __call__(self, event: MarketDataEvent) -> None:  # type: ignore[override]
        if event.channel_type != ChannelType.BOOK:
            return

        super().__call__(event)


class BookSnapshotHandler(BookHandler):
    def __call__(self, event: MarketDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.SNAPSHOT:
            return

        super().__call__(event)


class BookUpdateHandler(BookHandler):
    def __call__(self, event: MarketDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.UPDATE:
            return

        super().__call__(event)
