from ignis.options import options
from ignis.services.notifications import Notification, NotificationService
from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.modules.notification_center.player import MediaPlayer
from nomix.widgets.notification import NotificationWidget

notifications = NotificationService.get_default()


class Popup(Widget.Revealer):
    def __init__(self, notification: Notification, **kwargs):
        super().__init__(
            child=NotificationWidget(notification),
            transition_type="slide_down",
            **kwargs,
        )

        notification.connect("closed", lambda _: self.destroy())

    def destroy(self):
        self.reveal_child = False
        Utils.Timeout(self.transition_duration, self.unparent)


class NotificationList(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes=["notification-list"],
            vertical=True,
            vexpand=True,
            setup=lambda _: notifications.connect(
                "notified",
                lambda _, notification: self._on_notified(notification),
            ),
            child=[
                Widget.Label(
                    css_classes=["info-label"],
                    label="No notifications",
                    valign="center",
                    vexpand=True,
                    visible=notifications.bind(
                        "notifications", lambda value: len(value) == 0
                    ),
                ),
            ],
        )

        for n in notifications.notifications:
            self.append(Popup(n, reveal_child=True))

    def _on_notified(self, notification: Notification) -> None:
        popup = Popup(notification)
        self.prepend(popup)
        popup.reveal_child = True


class NotificationPanel(Widget.Box):
    def __init__(self, header_reverse: bool = False):
        header = Widget.Box(
            css_classes=["header"],
            child=[
                Widget.Box(
                    css_classes=["dnd"],
                    halign="start",
                    child=[
                        Widget.Switch(
                            active=options.notifications.bind("dnd"),
                            on_change=lambda _, active: options.notifications.set_dnd(
                                active
                            ),
                        ),
                        Widget.Label(label="Do Not Disturb"),
                    ],
                ),
                Widget.Button(
                    css_classes=["clear-all"],
                    label="Clear",
                    halign="end",
                    hexpand=True,
                    on_click=lambda _: notifications.clear_all(),
                ),
            ],
        )

        super().__init__(
            css_classes=["notification-center"],
            vertical=True,
            child=[
                header if header_reverse else None,
                Widget.Scroll(
                    vexpand=True,
                    child=Widget.Box(
                        vertical=True,
                        child=[
                            MediaPlayer(),
                            NotificationList(),
                        ],
                    ),
                ),
                header if not header_reverse else None,
            ],
        )
