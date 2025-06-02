import datetime

from ignis.services.notifications import Notification
from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.utils.helpers import AppInfo


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
            css_classes=["body"],
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

        app_name = notification.app_name
        app_icon = ""

        if desktop := AppInfo.from_app_name(notification.app_name):
            app_name = desktop.name

            if desktop.symbolic_icon:
                app_icon = desktop.symbolic_icon

        header = Widget.Box(
            css_classes=["notification-header"],
            child=[
                Widget.EventBox(
                    on_click=lambda _: notification.close(),
                    hexpand=True,
                    child=[
                        Widget.Icon(
                            css_classes=["app-icon"],
                            image=app_icon,
                            pixel_size=15,
                            visible=bool(app_icon),
                        ),
                        Widget.Label(
                            css_classes=["app-name"],
                            label=app_name,
                            visible=bool(app_name),
                            halign="start",
                        ),
                        Widget.Label(
                            css_classes=["time"],
                            label=Utils.Poll(1000, lambda _: _format_time()).bind(
                                "output"
                            ),
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
                                direction="down",
                                degree=180,
                                pixel_size=24,
                                rotated=self.body.bind(
                                    "ellipsize",
                                    lambda v: True if v == "none" else False,
                                ),
                            ),
                        ),
                        Widget.Button(
                            child=Widget.Icon(
                                image="window-close-symbolic", pixel_size=24
                            ),
                            on_click=lambda _: notification.close(),
                        ),
                    ],
                ),
            ],
        )

        center = Widget.EventBox(
            css_classes=["information"],
            on_click=lambda _: notification.close(),
            child=[
                Widget.Icon(
                    css_classes=["icon"],
                    image=notification.icon
                    if notification.icon
                    else "dialog-information-symbolic",
                    pixel_size=50,
                    halign="start",
                    valign="start",
                ),
                Widget.Box(
                    vertical=True,
                    hexpand=True,
                    child=[
                        Widget.Label(
                            label=notification.summary,
                            visible=notification.summary != "",
                            ellipsize="end",
                            halign="start",
                            css_classes=["summary"],
                        ),
                        self.body,
                    ],
                ),
            ],
        )

        actions = Widget.Box(
            css_classes=["actions"],
            child=[
                Widget.Button(
                    on_click=lambda _, action=action: action.invoke(),
                    child=Widget.Label(label=action.label),
                )
                for action in notification.actions
            ],
            homogeneous=True,
        )

        super().__init__(
            css_classes=["notification", *css_classes],
            vertical=True,
            hexpand=True,
            on_hover=lambda _: expand_on_hover and self._expand_body(True),
            on_hover_lost=lambda _: expand_on_hover and self._expand_body(False),
            child=[
                header,
                center,
                actions,
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
