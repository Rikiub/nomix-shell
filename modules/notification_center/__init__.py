from modules.types import ALIGN, WindowName
from widgets.popup_window import PopupWindow

from modules.notification_center.panel import NotificationPanel


class NotificationCenter(PopupWindow):
    def __init__(self, valign: ALIGN = "start", halign: ALIGN = "end"):
        super().__init__(
            namespace=WindowName.notification_center,
            css_classes=["notification-center"],
            valign=valign,
            halign=halign,
            child=[NotificationPanel()],
        )
