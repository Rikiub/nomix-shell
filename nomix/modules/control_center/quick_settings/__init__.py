from ignis.services.network import NetworkService
from ignis.widgets import Widget

from nomix.modules.control_center.quick_settings.night import night_light_control
from nomix.modules.control_center.quick_settings.vpn import vpn_control
from nomix.widgets.qsbutton import QSButton

from .bluetooth import bluetooth_control
from .dark import DarkModeQS
from .ethernet import ethernet_control
from .wifi import wifi_control

network = NetworkService.get_default()


class QuickSettings(Widget.Box):
    def __init__(self):
        super().__init__(vertical=True, css_classes=["quick-settings"])

        network.wifi.connect("notify::devices", lambda x, y: self._refresh())
        network.ethernet.connect("notify::devices", lambda x, y: self._refresh())
        network.vpn.connect("notify::connections", lambda x, y: self._refresh())

        self._refresh()

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
        row = Widget.Box(homogeneous=True)

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
        self, row: Widget.Box, button: QSButton, buttons: tuple[QSButton, ...], i: int
    ) -> None:
        row.append(button)

        if button.menu:
            self.append(button.menu)

            if i == len(buttons) - 1 or i == len(buttons) - 2:
                button.menu.box.add_css_class("qs-button-last-row")
