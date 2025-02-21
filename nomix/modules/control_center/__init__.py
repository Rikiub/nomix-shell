from ignis.app import IgnisApp
from ignis.widgets import Widget

from nomix.modules.control_center.battery import BatteryStatus
from nomix.modules.control_center.brightness import Brightness
from nomix.modules.control_center.power import PowerButton
from nomix.modules.control_center.quick_settings import QuickSettings
from nomix.modules.control_center.volume import Volume
from nomix.utils.constants import ModuleWindow
from nomix.utils.types import ALIGN
from nomix.widgets.menu import OPENED_MENU
from nomix.widgets.popup_window import PopupWindow

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
            namespace=ModuleWindow.control_center,
            on_close=lambda: OPENED_MENU.set_value(""),
            css_classes=["control-center"],
            valign=valign,
            halign=halign,
            child=[actions, sliders, QuickSettings()],
        )
