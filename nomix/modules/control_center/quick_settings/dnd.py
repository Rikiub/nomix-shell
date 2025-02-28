from ignis.options import options
from ignis.services.notifications import NotificationService

from nomix.widgets.qsbutton import QSButton

notifications = NotificationService.get_default()


class DNDQS(QSButton):
    def __init__(self):
        super().__init__(
            title=options.notifications.bind(
                "dnd", lambda value: "Silent" if value else "Noisy"
            ),
            icon_name=options.notifications.bind(
                "dnd",
                lambda value: "notification-disabled-symbolic"
                if value
                else "notification-symbolic",
            ),
            on_activate=lambda _: self._toggle(True),
            on_deactivate=lambda _: self._toggle(False),
            active=options.notifications.bind("dnd"),
        )

    def _toggle(self, state: bool) -> None:
        options.notifications.dnd = state
