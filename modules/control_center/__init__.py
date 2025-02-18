from ignis.app import IgnisApp
from ignis.widgets import Widget

from modules.control_center.battery import BatteryStatus
from modules.control_center.brightness import Brightness
from modules.control_center.quick_settings import QuickSettings
from modules.control_center.volume import Volume
from modules.utils import ALIGN, WindowName
from widgets.menu import OPENED_MENU
from widgets.popup_window import PopupWindow
from modules.control_center.power import PowerButton

app = IgnisApp.get_default()

class ControlCenter(PopupWindow):
    def __init__(self, valign: ALIGN = "start", halign: ALIGN = "center"):
        power = PowerButton(hexpand=True, halign="end")

        sliders = Widget.Box(
            vertical=True,
            css_classes=["slider-control"],
            child=[
                Volume("speaker"),
                Brightness(),
            ],
        )
        actions = Widget.Box(
            vertical=True,
            child=[
                Widget.Box(
                    css_classes=["actions"],
                    child=[BatteryStatus(), power],
                ),
                power.menu,
            ],
        )

        super().__init__(
            namespace=WindowName.control_center,
            on_close=lambda: OPENED_MENU.set_value(""),
            css_classes=["control-center"],
            valign=valign,
            halign=halign,
            child=[actions, sliders, QuickSettings()],
        )
