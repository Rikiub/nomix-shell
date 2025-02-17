from ignis.services.notifications import Notification
from ignis.variable import Variable
from ignis.widgets import Widget


class NotificationWidget(Widget.Box):
    def __init__(self, notification: Notification) -> None:
        self.ellipsize = Variable(False)

        self.body = Widget.Label(
            label=notification.body,
            ellipsize="end",
            halign="start",
            wrap="word",
            justify="left",
            css_classes=["notification-body"],
            visible=notification.body != "",
        )

        super().__init__(
            vertical=True,
            hexpand=True,
            css_classes=["notification"],
            child=[
                Widget.Box(
                    css_classes=["notification-header"],
                    child=[
                        Widget.Label(label=notification.app_name, halign="start"),
                        Widget.Box(
                            halign="end",
                            hexpand=True,
                            child=[
                                Widget.Button(
                                    on_click=lambda _: self._toggle_body(),
                                    child=Widget.Arrow(
                                        pixel_size=20,
                                        rotated=self.ellipsize.bind("value"),
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
                Widget.Box(
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
                            on_click=lambda x, action=action: action.invoke(),
                            css_classes=["notification-action"],
                        )
                        for action in notification.actions
                    ],
                    homogeneous=True,
                    style="margin-top: 0.75rem;" if notification.actions else "",
                    spacing=10,
                ),
            ],
        )

    def _toggle_body(self):
        if self.ellipsize.value:
            self.body.set_ellipsize("end")  # type: ignore
        else:
            self.body.set_ellipsize("none")  # type: ignore

        self.ellipsize.value = not self.ellipsize.value
