from ..data import MarketDataEvent
from ..enums import ChannelType
from ..enums import EventType
from .handler import Handler


class KLineHandler(Handler):
    def __call__(self, event: MarketDataEvent) -> None:  # type: ignore[override]
        if event.channel_type != ChannelType.KLINE:
            return

        super().__call__(event)


class KLineSnapshotHandler(KLineHandler):
    def __call__(self, event: MarketDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.SNAPSHOT:
            return

        super().__call__(event)


class KLineUpdateHandler(KLineHandler):
    def __call__(self, event: MarketDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.UPDATE:
            return

        super().__call__(event)
