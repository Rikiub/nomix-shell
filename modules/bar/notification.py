from ignis.app import IgnisApp
from ignis.widgets import Widget
from ignis.services.notifications import NotificationService

from modules.types import WindowName

notification = NotificationService.get_default()

app = IgnisApp.get_default()


class NotificationIcon(Widget.Button):
    def __init__(self, **kwargs):
        self.counter = 0
        self._label = Widget.Label(label="")

        super().__init__(
            on_click=lambda _: self._on_open(),
            setup=lambda *_: notification.connect(
                "new-popup", lambda *_: self._on_new()
            ),
            tooltip_text="Open notification center",
            child=Widget.Box(
                child=[
                    Widget.Icon(image="notification-symbolic", style="margin: 0 3px;"),
                    self._label,
                ]
            ),
            **kwargs,
        )

    def _on_open(self):
        app.toggle_window(WindowName.notification_center)

        self.counter = 0
        self._label.set_label("")

    def _on_new(self):
        self.counter += 1
        self._label.set_label(str(self.counter))
