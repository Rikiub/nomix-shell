from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice

from modules.control.quick_settings.qsbutton import QSButton
from widgets.menu_devices import DeviceMenu, DeviceItem
from widgets.toggle_box import ToggleBox

network = NetworkService.get_default()


class WifiItem(DeviceItem):
    def __init__(self, access_point: WifiAccessPoint):
        super().__init__(
            on_click=lambda x: access_point.connect_to_graphical(),
            icon_name=access_point.bind(
                "strength", transform=lambda value: access_point.icon_name
            ),
            label=access_point.ssid,
            active=access_point.bind("is_connected"),
        )


class WifiMenu(DeviceMenu):
    def __init__(self, device: WifiDevice):
        super().__init__(
            name="wifi",
            header=ToggleBox(
                label="Wi-Fi",
                active=network.wifi.enabled,
                on_change=lambda x, state: network.wifi.set_enabled(state),
            ),
            devices=device.bind(
                "access_points",
                transform=lambda value: [WifiItem(i) for i in value],
            ),
            settings_label="Network Settings",
            settings_command="nm-connection-editor",
        )


class WifiQS(QSButton):
    def __init__(self, device: WifiDevice):
        menu = WifiMenu(device)

        def get_label(ssid: str) -> str:
            if ssid:
                return ssid
            else:
                return "Wi-Fi"

        def get_icon(icon_name: str) -> str:
            if device.ap.is_connected:
                return icon_name
            else:
                return "network-wireless-symbolic"

        def toggle_list(x) -> None:
            device.scan()
            menu.toggle()

        super().__init__(
            label=device.ap.bind("ssid", get_label),
            icon_name=device.ap.bind("icon-name", get_icon),
            on_activate=toggle_list,
            on_deactivate=toggle_list,
            active=network.wifi.bind("enabled"),
            menu=menu,
        )


def wifi_control() -> list[QSButton]:
    return [WifiQS(dev) for dev in network.wifi.devices]
