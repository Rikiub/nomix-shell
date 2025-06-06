from gi.repository import GLib  # type: ignore
from ignis.services.notifications import Notification, NotificationService
from ignis.utils.timeout import Timeout
from ignis.widgets import Widget

from nomix.widgets.base_view import ListView
from nomix.widgets.notification import NotificationWidget


notifications = NotificationService.get_default()


class NotificationList(ListView):
    def __init__(
        self,
        only_popups: bool = False,
        css_classes: list[str] = [],
        control=None,
        **kwargs,
    ):
        def on_bind(revealer: Widget.Revealer, notify: Notification):
            child = revealer.child
            child.update(notify)

            def close():
                revealer.reveal_child = False
                Timeout(
                    revealer.transition_duration,
                    lambda: self.remove_item(notify),
                )

            child.on_close = close
            if only_popups:
                notify.connect(
                    "dismissed",
                    lambda _: close(),
                )

            GLib.idle_add(lambda: revealer.set_reveal_child(True))

        super().__init__(
            item_type=Notification,
            items=notifications.notifications if not only_popups else [],
            on_setup=lambda: Widget.Revealer(
                reveal_child=False,
                transition_type="slide_down",
                transition_duration=300,
                child=NotificationWidget(css_classes=["popup" if only_popups else ""]),
            ),
            on_bind=on_bind,
            css_classes=["notification-list", *css_classes],
            **kwargs,
        )

        signal = "notified"
        if only_popups:
            signal = "new_popup"

        notifications.connect(
            signal,
            lambda _, notify: self.append_item(notify),
        )
