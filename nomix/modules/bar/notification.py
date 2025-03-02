from ignis.options import options
from ignis.services.mpris import MprisService
from ignis.services.notifications import NotificationService
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.widgets.actionable_button import ActionableButton

notification = NotificationService.get_default()
mpris = MprisService.get_default()


class NotificationCenterButton(ActionableButton):
    def __init__(self):
        self.counter = 0
        self._label = Widget.Label(label="")

        super().__init__(
            on_click=lambda _: self._on_open(),
            toggle_window=ModuleWindow.NOTIFICATION_CENTER,
            setup=lambda *_: notification.connect(
                "new-popup", lambda *_: self._on_new()
            ),
            tooltip_text="Notification Center",
            css_classes=["notification-center-button"],
            child=Widget.Box(
                child=[
                    Widget.Icon(
                        image="multimedia-player-symbolic",
                        visible=mpris.bind("players", lambda v: bool(v)),
                    ),
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
        )

    def _on_open(self):
        self.counter = 0
        self._label.set_label("")

    def _on_new(self):
        self.counter += 1
        self._label.set_label(str(self.counter))
