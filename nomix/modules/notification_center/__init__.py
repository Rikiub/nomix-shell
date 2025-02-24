
from nomix.modules.notification_center.panel import NotificationPanel
from nomix.utils.constants import ModuleWindow
from nomix.utils.types import ALIGN
from nomix.widgets.popup_window import PopupWindow


class NotificationCenter(PopupWindow):
    def __init__(self, valign: ALIGN = "start", halign: ALIGN = "end"):
        super().__init__(
            namespace=ModuleWindow.notification_center,
            css_classes=["notification-center"],
            valign=valign,
            halign=halign,
            child=[NotificationPanel(header_reverse=True)],
        )
