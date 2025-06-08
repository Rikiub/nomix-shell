from __future__ import annotations

from ignis import widgets
from ignis.app import IgnisApp
from ignis.services.notifications import NotificationService

from nomix.utils.types import ANCHOR
from nomix.widgets.notification_list import NotificationList

app = IgnisApp.get_default()
notifications = NotificationService.get_default()


class NotificationPopup(widgets.Window):
    def __init__(
        self,
        monitor: int = 0,
        anchor: list[ANCHOR] = ["top", "right"],
    ):
        super().__init__(
            css_classes=["transparent"],
            namespace=f"notification_popup_{monitor}",
            layer="top",
            anchor=anchor,  # type: ignore
            monitor=monitor,
            child=NotificationList(only_popups=True),
        )
