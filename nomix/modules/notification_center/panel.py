from ignis.options import options
from ignis.services.notifications import NotificationService
from ignis.widgets import Widget

from nomix.modules.notification_center.player import MediaPlayer
from nomix.widgets.notification_list import NotificationList

notifications = NotificationService.get_default()


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

        container = Widget.Box(
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
        )

        super().__init__(
            css_classes=["notification-center"],
            vertical=True,
            child=[
                header if header_reverse else None,
                Widget.Scroll(vexpand=True, child=container),
                header if not header_reverse else None,
            ],
        )
