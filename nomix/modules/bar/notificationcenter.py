from ignis.options import options
from ignis.services.mpris import MprisService
from ignis.services.notifications import Notification, NotificationService
from ignis.variable import Variable
from ignis import widgets

from nomix.utils.constants import ModuleWindow
from nomix.widgets.action_button import ActionButton

notification = NotificationService.get_default()
mpris = MprisService.get_default()


class NotificationCenter(ActionButton):
    def __init__(self, css_classes: list[str] = []):
        self._counter = Variable(0)
        self._label = widgets.Label(label="")

        def tooltip_text():
            text = "Notification Center"
            count = self._counter.value

            if count > 0:
                text = f"{text}\n{count} notifications unread"

            return text

        super().__init__(
            css_classes=["notification-center-button", *css_classes],
            tooltip_text=self._counter.bind("value", lambda _: tooltip_text()),
            toggle_window=ModuleWindow.NOTIFICATION_CENTER,
            on_click=lambda _: self._reset(),
            child=widgets.Box(
                halign="center",
                hexpand=True,
                child=[
                    widgets.Icon(
                        image="media-playback-start-symbolic",
                        visible=mpris.bind("players", lambda v: bool(v)),
                    ),
                    widgets.Icon(
                        image=options.notifications.bind(  # type: ignore
                            "dnd",
                            lambda v: "notification-disabled-symbolic"
                            if v
                            else "notification-symbolic",
                        ),
                        visible=self._counter.bind(
                            "value",
                            lambda v: v == 0,
                        ),
                    ),
                    widgets.Icon(
                        image="notification-new-symbolic",
                        visible=self._counter.bind(
                            "value",
                            lambda v: v > 0,
                        ),
                    ),
                ],
            ),
        )

        notification.connect("new-popup", lambda _, v: self._on_notify(v))

    def _on_notify(self, notify: Notification):
        self._increment()
        notify.connect("closed", lambda *_: self._decrement())

    def _increment(self):
        self._counter.value += 1
        self._sync()

    def _decrement(self):
        if self._counter.value > 0:
            self._counter.value -= 1
            self._sync()

    def _reset(self):
        self._counter.value = 0
        self._sync()

    def _sync(self):
        text = "" if self._counter.value == 0 else self._counter.value
        text = str(text)

        self._label.set_label(text)
