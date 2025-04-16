from datetime import datetime

from domains.fabzenda import messages as MSG


class FabzendaSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def fabzenda_option(self) -> str:
        return MSG.FABZENDA_OPTIONS
