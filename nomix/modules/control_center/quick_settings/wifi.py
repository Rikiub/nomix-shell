import asyncio

from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.widgets import Widget

from nomix.utils.global_options import user_options
from nomix.widgets.header_label import HeaderLabel
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu
from nomix.widgets.qsbutton import QSButton

network = NetworkService.get_default()


class WifiItem(DeviceItem):
    def __init__(self, access_point: WifiAccessPoint):
        super().__init__(
            label=access_point.ssid,
            icon_name=access_point.bind("strength", lambda _: access_point.icon_name),
            extra_icon_name="changes-prevent-symbolic"
            if access_point.security
            else "changes-allow-symbolic",
            active=access_point.bind("is_connected"),
            on_click=lambda _: self.toggle(access_point),
            extra_widget=Widget.Button(
                tooltip_text="Click to Forget",
                on_click=lambda _: asyncio.create_task(access_point.forget()),
                child=Widget.Icon(image="dialog-password-symbolic"),
                visible=access_point.bind("psk", lambda v: bool(v)),
            ),
        )

    def toggle(self, access_point: WifiAccessPoint):
        if access_point.is_connected:
            asyncio.create_task(access_point.disconnect_from())
        else:
            asyncio.create_task(access_point.connect_to_graphical())


class WifiMenu(DeviceMenu):
    def __init__(self, device: WifiDevice):
        super().__init__(
            name="wifi",
            header=HeaderLabel(
                icon_name="network-wireless-symbolic",
                label="Wi-Fi",
                active=network.wifi.bind("enabled"),
            ),
            placeholder=network.wifi.bind(
                "enabled",
                lambda enabled: "No Wi-Fi networks found"
                if enabled
                else "Turn on Wi-Fi to view available networks",
            ),
            devices=device.bind(
                "access_points",
                transform=lambda value: [WifiItem(i) for i in value],
            ),
            settings_label="Network Settings",
            settings_command=user_options.control_apps.network,
        )


class WifiQS(QSButton):
    def __init__(self, device: WifiDevice):
        super().__init__(
            title="Wi-Fi",
            subtitle=device.ap.bind("ssid"),
            icon_name=device.ap.bind("icon-name", lambda v: v),
            on_activate=lambda _: network.wifi.set_enabled(True),
            on_deactivate=lambda _: network.wifi.set_enabled(False),
            active=network.wifi.bind("enabled"),
            menu=WifiMenu(device),
        )


def wifi_control() -> list[QSButton]:
    return [WifiQS(dev) for dev in network.wifi.devices]
