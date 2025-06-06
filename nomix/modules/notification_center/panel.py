from gi.repository import GLib  # type: ignore
from ignis.options import options
from ignis.services.notifications import Notification, NotificationService
from ignis.utils.timeout import Timeout
from ignis.widgets import Widget

from nomix.modules.notification_center.player import MediaPlayer
from nomix.widgets.base_view import ListView
from nomix.widgets.notification import NotificationWidget

notifications = NotificationService.get_default()


class NotificationList(ListView):
    def __init__(self, css_classes: list[str] = [], **kwargs):
        def on_bind(revealer: Widget.Revealer, notify: Notification):
            child = revealer.child
            child.update(notify)

            def close():
                revealer.reveal_child = False
                Timeout(revealer.transition_duration, lambda: self.remove_item(notify))

            child.on_close = close
            GLib.idle_add(lambda: revealer.set_reveal_child(True))

        super().__init__(
            item_type=Notification,
            items=notifications.notifications,
            on_setup=lambda: Widget.Revealer(
                reveal_child=False,
                transition_type="slide_down",
                transition_duration=300,
                child=NotificationWidget(),
            ),
            on_bind=on_bind,
            css_classes=["notification-list", *css_classes],
            **kwargs,
        )

        notifications.connect(
            "notified",
            lambda _, notify: self.append_item(notify),
        )


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
                            active=options.notifications.bind("dnd"),  # type: ignore
                            on_change=lambda _, active: options.notifications.set_dnd(  # type: ignore
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
                            Widget.Revealer(
                                vexpand=True,
                                valign="center",
                                transition_type="crossfade",
                                transition_duration=700,
                                reveal_child=notifications.bind(
                                    "notifications",
                                    lambda v: len(v) == 0,
                                ),
                                child=Widget.Label(
                                    css_classes=["info-label"],
                                    label="No notifications",
                                ),
                            ),
                        ],
                    ),
                ),
                header if not header_reverse else None,
            ],
        )
