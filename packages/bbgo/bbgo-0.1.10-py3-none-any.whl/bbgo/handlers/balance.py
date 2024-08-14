from ..data import UserDataEvent
from ..enums import ChannelType
from ..enums import EventType
from .handler import Handler


class BalanceHandler(Handler):
    def __call__(self, event: UserDataEvent) -> None:  # type: ignore[override]
        if event.channel_type != ChannelType.BALANCE:
            return

        super().__call__(event)


class BalanceSnapshotHandler(BalanceHandler):
    def __call__(self, event: UserDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.SNAPSHOT:
            return

        super().__call__(event)


class BalanceUpdateHandler(BalanceHandler):
    def __call__(self, event: UserDataEvent) -> None:  # type: ignore[override]
        if event.event_type != EventType.UPDATE:
            return

        super().__call__(event)
