from ignis.app import IgnisApp
from ignis.widgets import Widget

from nomix.modules.control_center.battery import BatteryStatus
from nomix.modules.control_center.brightness import Brightness
from nomix.modules.control_center.lock import LockButton
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
        power = PowerButton()

        actions_left = Widget.Box(
            child=[BatteryStatus()],
            css_classes=["left"],
        )
        actions_right = Widget.Box(
            child=[LockButton(), power],
            hexpand=True,
            halign="end",
            css_classes=["right"],
        )
        actions = Widget.Box(
            css_classes=["actions"],
            child=[actions_left, actions_right],
        )

        super().__init__(
            namespace=ModuleWindow.CONTROL_CENTER,
            on_close=lambda: OPENED_MENU.set_value(""),
            css_classes=["control-center"],
            width_request=450,
            valign=valign,
            halign=halign,
            child=[
                Widget.Box(
                    vertical=True,
                    child=[
                        actions,
                        power.menu,
                    ],
                ),
                Widget.Box(
                    vertical=True,
                    css_classes=["slider-control"],
                    child=[
                        Volume("speaker"),
                        Brightness(),
                    ],
                ),
                QuickSettings(),
            ],
        )
