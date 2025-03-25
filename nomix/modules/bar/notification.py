from ignis.options import options
from ignis.services.mpris import MprisService
from ignis.services.notifications import Notification, NotificationService
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.widgets.actionable_button import ActionableButton

notification = NotificationService.get_default()
mpris = MprisService.get_default()


class NotificationCenterButton(ActionableButton):
    def __init__(self):
        self._counter = 0
        self._label = Widget.Label(label="")

        super().__init__(
            toggle_window=ModuleWindow.NOTIFICATION_CENTER,
            on_click=lambda _: self._reset(),
            tooltip_text="Notification Center",
            css_classes=["notification-center-button"],
            child=Widget.Box(
                child=[
                    Widget.Icon(
                        image="media-playback-start-symbolic",
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

        notification.connect("new-popup", lambda _, v: self._on_notify(v))

    def _on_notify(self, notify: Notification):
        self._increment()
        notify.connect("closed", lambda *_: self._decrement())

    def _increment(self):
        self._counter += 1
        self._sync()

    def _decrement(self):
        if self._counter > 0:
            self._counter -= 1
            self._sync()

    def _reset(self):
        self._counter = 0
        self._sync()

    def _sync(self):
        text = "" if self._counter == 0 else self._counter
        text = str(text)

        self._label.set_label(text)
