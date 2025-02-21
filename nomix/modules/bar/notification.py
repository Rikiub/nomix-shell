from ignis.app import IgnisApp
from ignis.options import options
from ignis.services.notifications import NotificationService
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow

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
            tooltip_text="Notification center",
            child=Widget.Box(
                child=[
                    Widget.Icon(
                        image=options.notifications.bind(
                            "dnd",
                            lambda v: "notification-disabled-symbolic"
                            if v
                            else "notification-symbolic",
                        ),
                        style="margin: 0 3px;",
                    ),
                    self._label,
                ]
            ),
            **kwargs,
        )

    def _on_open(self):
        app.toggle_window(ModuleWindow.notification_center)

        self.counter = 0
        self._label.set_label("")

    def _on_new(self):
        self.counter += 1
        self._label.set_label(str(self.counter))
