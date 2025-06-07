from ignis.options import options
from ignis.services.notifications import NotificationService
from ignis import widgets

from nomix.modules.notification_center.player import MediaPlayer
from nomix.widgets.notification_list import NotificationList

notifications = NotificationService.get_default()


class NotificationPanel(widgets.Box):
    def __init__(self, header_reverse: bool = False):
        header = widgets.Box(
            css_classes=["header"],
            child=[
                widgets.Box(
                    css_classes=["dnd"],
                    halign="start",
                    child=[
                        widgets.Switch(
                            active=options.notifications.bind("dnd"),  # type: ignore
                            on_change=lambda _, active: options.notifications.set_dnd(  # type: ignore
                                active
                            ),
                        ),
                        widgets.Label(label="Do Not Disturb"),
                    ],
                ),
                widgets.Button(
                    css_classes=["clear-all"],
                    label="Clear",
                    halign="end",
                    hexpand=True,
                    on_click=lambda _: notifications.clear_all(),
                ),
            ],
        )

        container = widgets.Box(
            vertical=True,
            child=[
                MediaPlayer(),
                NotificationList(),
                widgets.Revealer(
                    vexpand=True,
                    valign="center",
                    transition_type="crossfade",
                    transition_duration=700,
                    reveal_child=notifications.bind(
                        "notifications",
                        lambda v: len(v) == 0,
                    ),
                    child=widgets.Label(
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
                widgets.Scroll(vexpand=True, child=container),
                header if not header_reverse else None,
            ],
        )
