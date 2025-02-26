from __future__ import annotations

from ignis.app import IgnisApp
from ignis.services.notifications import Notification, NotificationService
from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.utils.types import ANCHOR
from nomix.widgets.notification import NotificationWidget

app = IgnisApp.get_default()
notifications = NotificationService.get_default()


class Popup(Widget.Box):
    def __init__(self, window: NotificationPopup, notification: Notification):
        self._window = window

        widget = NotificationWidget(notification, css_classes=["notification-popup"])

        self.inner = Widget.Revealer(transition_type="slide_down", child=widget)
        self.outer = Widget.Revealer(transition_type="slide_up", child=self.inner)

        super().__init__(child=[self.outer], style="background-color: transparent;")

        notification.connect("dismissed", lambda _: self.destroy())

    def destroy(self):
        def popup_destroy():
            self.unparent()
            if len(notifications.popups) == 0:
                self._window.visible = False

        def outer_close():
            self.outer.reveal_child = False
            Utils.Timeout(self.outer.transition_duration, popup_destroy)

        self.inner.transition_type = "crossfade"
        self.inner.reveal_child = False

        Utils.Timeout(self.outer.transition_duration, outer_close)


class NotificationPopup(Widget.Window):
    def __init__(self, monitor: int = 0, anchor: list[ANCHOR] = ["top", "right"]):
        self.box = Widget.Box(
            vertical=True,
            setup=lambda _: notifications.connect(
                "new_popup", lambda _, notification: self._on_notified(notification)
            ),
        )

        super().__init__(
            namespace=f"notification_popup_{monitor}",
            layer="top",
            anchor=anchor,  # type: ignore
            monitor=monitor,
            visible=False,
            child=self.box,
            style="background-color: transparent; border: unset;",
        )

    def _on_notified(self, notification: Notification) -> None:
        self.visible = True

        popup = Popup(window=self, notification=notification)
        self.box.prepend(popup)
        popup.outer.reveal_child = True

        Utils.Timeout(
            popup.outer.transition_duration, popup.inner.set_reveal_child, True
        )