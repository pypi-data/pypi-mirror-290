from ..data import Event


class Handler:

    def __call__(self, event: Event) -> None:
        self.handle(event)

    def handle(self, event: Event) -> None:
        raise NotImplementedError
