from ignis.app import IgnisApp
from ignis.widgets import Widget

from modules.control_center.battery import BatteryStatus
from modules.control_center.brightness import Brightness
from modules.control_center.quick_settings import QuickSettings
from modules.control_center.volume import Volume
from modules.types import ALIGN, WindowName
from widgets.menu import opened_menu
from widgets.popup_window import PopupWindow
from widgets.powermenu import PowerMenu

app = IgnisApp.get_default()


class ControlCenter(PopupWindow):
    def __init__(self, valign: ALIGN = "start", halign: ALIGN = "center"):
        super().__init__(
            namespace=WindowName.control_center,
            on_close=lambda: opened_menu.set_value(""),
            css_classes=["control-center"],
            valign=valign,
            halign=halign,
            child=[
                Widget.Box(
                    css_classes=["actions"],
                    child=[BatteryStatus(), PowerMenu(halign="end", hexpand=True)],
                ),
                Volume("speaker"),
                Brightness(),
                QuickSettings(),
            ],
        )
