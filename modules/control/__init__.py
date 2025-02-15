from ignis.app import IgnisApp
from ignis.widgets import Widget

from modules.control.brightness import Brightness
from modules.control.notification_center import NotificationCenter
from modules.control.quick_settings import QuickSettings
from modules.control.volume import Volume
from modules.types import ALIGN, WindowName
from widgets.menu import opened_menu
from widgets.popup_window import PopupWindow
from widgets.powermenu import PowerMenu

app = IgnisApp.get_default()


class ControlPanel(PopupWindow):
    def __init__(
        self,
        valign: ALIGN = "start",
        halign: ALIGN = "center",
    ):
        super().__init__(
            namespace=WindowName.control,
            on_close=lambda: opened_menu.set_value(""),
            overlays=[
                Widget.Box(
                    css_classes=["control"],
                    valign=valign,
                    halign=halign,
                    vertical=True,
                    child=[
                        PowerMenu(halign="end"),
                        Volume("speaker"),
                        Brightness(),
                        QuickSettings(),
                        NotificationCenter(),
                    ],
                )
            ],
        )
