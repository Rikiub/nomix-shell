import datetime

from ignis.services.notifications import Notification
from ignis.utils import Utils
from ignis.widgets import Widget


class NotificationWidget(Widget.EventBox):
    def __init__(
        self,
        notification: Notification,
        expand_on_hover: bool = False,
        css_classes: list[str] = [],
    ) -> None:
        self.body = Widget.Label(
            label=notification.body,
            use_markup=True,
            ellipsize="end",
            halign="start",
            wrap="word",
            justify="left",
            css_classes=["notification-body"],
            visible=notification.body != "",
        )

        def _get_past_time(timestamp: float) -> tuple[int, int, int]:
            current = datetime.datetime.now()
            past = datetime.datetime.fromtimestamp(timestamp)
            delta = current - past

            hours, remainder = divmod(delta.total_seconds(), 3600)

            hours = round(hours)
            minutes = round(remainder // 60)

            return delta.days, hours, minutes

        def _format_time() -> str:
            days, hours, minutes = _get_past_time(notification.time)

            if days:
                return f"{days} days ago"
            elif hours:
                return f"{hours} hours ago"
            elif minutes:
                return f"{minutes} minutes ago"
            else:
                return "Just now"

        super().__init__(
            vertical=True,
            hexpand=True,
            css_classes=["notification"] + css_classes,
            on_hover=lambda _: expand_on_hover and self._expand_body(True),
            on_hover_lost=lambda _: expand_on_hover and self._expand_body(False),
            child=[
                Widget.Box(
                    css_classes=["notification-header"],
                    child=[
                        Widget.EventBox(
                            on_click=lambda _: notification.close(),
                            hexpand=True,
                            child=[
                                Widget.Label(
                                    label=notification.app_name,
                                    halign="start",
                                    style="margin-right: 8px;",
                                    css_classes=["notification-app-name"],
                                ),
                                Widget.Label(
                                    label=Utils.Poll(
                                        1000, lambda _: _format_time()
                                    ).bind("output"),
                                    css_classes=["notification-time"],
                                ),
                            ],
                        ),
                        Widget.Box(
                            halign="end",
                            hexpand=True,
                            child=[
                                Widget.Button(
                                    on_click=lambda _: self._toggle_body(),
                                    child=Widget.Arrow(
                                        pixel_size=20,
                                        rotated=self.body.bind(
                                            "ellipsize",
                                            lambda v: True if v == "none" else False,
                                        ),
                                    ),
                                ),
                                Widget.Button(
                                    child=Widget.Icon(
                                        image="window-close-symbolic", pixel_size=20
                                    ),
                                    on_click=lambda _: notification.close(),
                                ),
                            ],
                        ),
                    ],
                ),
                Widget.EventBox(
                    on_click=lambda _: notification.close(),
                    child=[
                        Widget.Icon(
                            image=notification.icon
                            if notification.icon
                            else "dialog-information-symbolic",
                            pixel_size=40,
                            halign="start",
                            valign="start",
                        ),
                        Widget.Box(
                            vertical=True,
                            hexpand=True,
                            style="margin-left: 0.75rem;",
                            child=[
                                Widget.Label(
                                    label=notification.summary,
                                    visible=notification.summary != "",
                                    ellipsize="end",
                                    halign="start",
                                    css_classes=["notification-summary"],
                                ),
                                self.body,
                            ],
                        ),
                    ],
                ),
                Widget.Box(
                    child=[
                        Widget.Button(
                            child=Widget.Label(label=action.label),
                            on_click=lambda _, action=action: action.invoke(),
                            css_classes=["notification-action"],
                        )
                        for action in notification.actions
                    ],
                    spacing=10,
                    homogeneous=True,
                    style="margin-top: 0.75rem;" if notification.actions else "",
                ),
            ],
        )

    def _expand_body(self, value: bool):
        if value:
            self.body.set_ellipsize("none")  # type: ignore
        else:
            self.body.set_ellipsize("end")  # type: ignore

    def _toggle_body(self):
        if self.body.get_ellipsize() == "none":
            self._expand_body(False)
        else:
            self._expand_body(True)
