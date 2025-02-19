from gi.repository import GLib  # type: ignore
from ignis.options import options
from ignis.services.notifications import Notification, NotificationService
from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.widgets.notification import NotificationWidget

notifications = NotificationService.get_default()


class Popup(Widget.Revealer):
    def __init__(self, notification: Notification, **kwargs):
        widget = NotificationWidget(notification)
        super().__init__(child=widget, transition_type="slide_down", **kwargs)

        notification.connect("closed", lambda x: self.destroy())

    def destroy(self):
        self.reveal_child = False
        Utils.Timeout(self.transition_duration, self.unparent)


class NotificationList(Widget.Box):
    def __init__(self):
        loading_notifications_label = Widget.Label(
            label="Loading notifications...",
            valign="center",
            vexpand=True,
        )

        super().__init__(
            vertical=True,
            css_classes=["notification-list"],
            child=[loading_notifications_label],
            vexpand=True,
            setup=lambda self: notifications.connect(
                "notified",
                lambda x, notification: self._on_notified(notification),
            ),
        )

        Utils.ThreadTask(
            self._load_notifications,
            lambda result: self.set_child(result),
        ).run()

    def _on_notified(self, notification: Notification) -> None:
        notify = Popup(notification)
        self.prepend(notify)
        notify.reveal_child = True

    def _load_notifications(self) -> list[Widget.Label | Popup]:
        widgets: list[Widget.Label | Popup] = []
        for i in notifications.notifications:
            GLib.idle_add(lambda i=i: widgets.append(Popup(i, reveal_child=True)))

        widgets.append(
            Widget.Label(
                label="No notifications",
                valign="center",
                vexpand=True,
                visible=notifications.bind(
                    "notifications", lambda value: len(value) == 0
                ),
                css_classes=["info-label"],
            )
        )
        return widgets


class NotificationPanel(Widget.Box):
    def __init__(self):
        header = Widget.Box(
            css_classes=["header"],
            child=[
                Widget.Box(
                    css_classes=["dnd"],
                    halign="start",
                    child=[
                        Widget.Switch(
                            active=options.notifications.bind("dnd"),
                            on_change=lambda x, active: options.notifications.set_dnd(
                                active
                            ),
                        ),
                        Widget.Label(label="Do Not Disturb"),
                    ],
                ),
                Widget.Button(
                    label="Clear",
                    on_click=lambda x: notifications.clear_all(),
                    halign="end",
                    hexpand=True,
                    css_classes=["clear-all"],
                ),
            ],
        )

        super().__init__(
            vertical=True,
            vexpand=True,
            css_classes=["notification-center"],
            child=[
                header,
                Widget.Scroll(
                    child=NotificationList(),
                    vexpand=True,
                ),
            ],
        )
