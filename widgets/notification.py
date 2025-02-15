from ignis.services.notifications import Notification
from ignis.widgets import Widget


class NotificationWidget(Widget.Box):
    def __init__(self, notification: Notification) -> None:
        self.text_limit = 200

        super().__init__(
            vertical=True,
            hexpand=True,
            css_classes=["notification"],
            child=[
                Widget.Box(
                    child=[
                        Widget.Icon(
                            image=notification.icon
                            if notification.icon
                            else "dialog-information-symbolic",
                            pixel_size=48,
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
                                    css_classes=["summary"],
                                ),
                                Widget.Scroll(
                                    hexpand=True,
                                    child=Widget.Label(
                                        label=notification.body,
                                        wrap=True,
                                        halign="start",
                                        css_classes=["body"],
                                        visible=notification.body != "",
                                    ),
                                ),
                            ],
                        ),
                        Widget.Button(
                            child=Widget.Icon(
                                image="window-close-symbolic", pixel_size=20
                            ),
                            halign="end",
                            valign="start",
                            css_classes=["close"],
                            on_click=lambda x: notification.close(),
                        ),
                    ],
                ),
                Widget.Box(
                    child=[
                        Widget.Button(
                            child=Widget.Label(label=action.label),
                            on_click=lambda x, action=action: action.invoke(),
                            css_classes=["action"],
                        )
                        for action in notification.actions
                    ],
                    homogeneous=True,
                    style="margin-top: 0.75rem;" if notification.actions else "",
                    spacing=10,
                ),
            ],
        )

    def _ellipse(self, text: str) -> str:
        if len(text) > self.text_limit:
            return text[: self.text_limit] + "..."
        return text
