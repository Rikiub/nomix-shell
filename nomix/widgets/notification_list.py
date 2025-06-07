from gi.repository import GLib  # type: ignore
from ignis import widgets
from ignis.services.notifications import Notification, NotificationService
from ignis.utils.timeout import Timeout

from nomix.widgets.notification import NotificationWidget
from nomix.widgets.view import ListView

notifications = NotificationService.get_default()


class NotificationList(ListView):
    def __init__(
        self,
        only_popups: bool = False,
        css_classes: list[str] = [],
        control=None,
        **kwargs,
    ):
        def on_bind(revealer: widgets.Revealer, notify: Notification):
            child = revealer.child
            child.update(notify)

            def open():
                revealer.reveal_child = True
                return GLib.SOURCE_REMOVE

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

            GLib.idle_add(open)

        super().__init__(
            item_type=Notification,
            items=notifications.notifications if not only_popups else [],
            on_setup=lambda: widgets.Revealer(
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
