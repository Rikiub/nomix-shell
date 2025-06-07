from ignis import widgets
from ignis.services.bluetooth import BluetoothService
from ignis.services.network import NetworkService

from nomix.modules.control_center.quick_settings.night import night_light_control
from nomix.modules.control_center.quick_settings.vpn import vpn_control
from nomix.utils.options import USER_OPTIONS
from nomix.widgets.qsbutton import QSButton

from ..quick_settings.bluetooth import bluetooth_control
from .dark import DarkModeQS
from .ethernet import ethernet_control
from .wifi import wifi_control

network = NetworkService.get_default()
bluetooth = BluetoothService.get_default()


class QuickSettings(widgets.Box):
    def __init__(self):
        super().__init__(vertical=True, css_classes=["quick-settings"])

        self._refresh()

        network.wifi.connect("notify::devices", lambda *_: self._refresh())
        network.ethernet.connect("notify::devices", lambda *_: self._refresh())
        network.vpn.connect("notify::connections", lambda *_: self._refresh())

        USER_OPTIONS.night_light.connect_option("enabled", lambda *_: self._refresh())

        # Bluetooth
        self._bluetooth_available = False

        def sync_bluetooth():
            if bluetooth.state != "absent" and not self._bluetooth_available:
                self._bluetooth_available = True
                self._refresh()
            elif bluetooth.state == "absent" and self._bluetooth_available:
                self._bluetooth_available = False
                self._refresh()

        bluetooth.connect("notify::state", lambda *_: sync_bluetooth())

    def actions(self) -> list[QSButton]:
        return [
            *wifi_control(),
            *ethernet_control(),
            *vpn_control(),
            *bluetooth_control(),
            DarkModeQS(),
            *night_light_control(),
        ]

    def _refresh(self) -> None:
        self.child = []
        self._qs_fabric(*self.actions())

    def _qs_fabric(self, *buttons: QSButton) -> None:
        for i in range(0, len(buttons), 2):
            self._add_row(buttons, i)

    def _add_row(self, buttons: tuple[QSButton, ...], i: int) -> None:
        row = widgets.Box(homogeneous=True)

        if len(self.child) > 0:
            row.style = "margin-top: 0.7rem;"  # type: ignore

        self.append(row)

        button1 = buttons[i]

        self._add_button(row, button1, buttons, i)

        if i + 1 < len(buttons):
            button2 = buttons[i + 1]
            button2.style = "margin-left: 0.5rem;"  # type: ignore
            self._add_button(row, button2, buttons, i)

    def _add_button(
        self, row: widgets.Box, button: QSButton, buttons: tuple[QSButton, ...], i: int
    ) -> None:
        row.append(button)

        if button.menu:
            self.append(button.menu)

            if i == len(buttons) - 1 or i == len(buttons) - 2:
                button.menu.box.add_css_class("qs-button-last-row")
