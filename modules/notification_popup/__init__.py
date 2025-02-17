from __future__ import annotations

from ignis.app import IgnisApp
from ignis.services.notifications import Notification, NotificationService
from ignis.utils import Utils
from ignis.widgets import Widget

from modules.utils import ANCHOR
from widgets.notification import NotificationWidget

app = IgnisApp.get_default()
notifications = NotificationService.get_default()


class Popup(Widget.Box):
    def __init__(
        self, box: PopupBox, window: NotificationPopup, notification: Notification
    ):
        self._box = box
        self._window = window
        self.hover = False

        widget = NotificationWidget(notification)
        widget.css_classes = ["notification", "notification-popup"]

        self._inner = Widget.Revealer(transition_type="crossfade", child=widget)
        self._outer = Widget.Revealer(transition_type="crossfade", child=self._inner)

        super().__init__(
            child=[self._outer],
            halign="end",
        )

        notification.connect("dismissed", lambda x: self.destroy())

    def destroy(self):
        def box_destroy():
            self.unparent()
            if len(notifications.popups) == 0:
                self._window.visible = False

        def outer_close():
            self._outer.reveal_child = False
            Utils.Timeout(self._outer.transition_duration, box_destroy)

        self._inner.transition_type = "crossfade"
        self._inner.reveal_child = False
        Utils.Timeout(self._outer.transition_duration, outer_close)


class PopupBox(Widget.Box):
    def __init__(self, window: NotificationPopup, monitor: int):
        self._window = window
        self._monitor = monitor

        super().__init__(
            valign="start",
            vertical=True,
            setup=lambda self: notifications.connect(
                "new_popup",
                lambda x, notification: self._on_notified(notification),
            ),
        )

    def _on_notified(self, notification: Notification) -> None:
        self._window.visible = True
        popup = Popup(box=self, window=self._window, notification=notification)

        self.prepend(popup)
        popup._outer.reveal_child = True

        Utils.Timeout(
            popup._outer.transition_duration, popup._inner.set_reveal_child, True
        )


class NotificationPopup(Widget.Window):
    def __init__(self, monitor: int = 0, anchor: list[ANCHOR] = ["top", "right"]):
        super().__init__(
            anchor=anchor,  # type: ignore
            monitor=monitor,
            namespace=f"notification_popup_{monitor}",
            layer="top",
            visible=False,
            style="background-color: transparent;",
            child=PopupBox(window=self, monitor=monitor),
        )
