import asyncio

from ignis import utils, widgets
from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice

from nomix.utils.options import USER_OPTIONS
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
            extra_widget=widgets.Button(
                tooltip_text="Click to Forget",
                on_click=lambda _: asyncio.create_task(access_point.forget()),
                child=widgets.Icon(image="dialog-password-symbolic"),
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
            placeholder_text=network.wifi.bind(
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
            settings_command=USER_OPTIONS.control_center.settings_apps.bind("network"),  # type: ignore
        )


class WifiQS(QSButton):
    def __init__(self, device: WifiDevice):
        self._auto_scan = False
        self._device = device

        def subtitle(is_connected: bool, ssid: str | None) -> str | None:
            if is_connected and ssid:
                return device.ap.ssid
            else:
                return None

        def on_opened(opened: bool):
            self._auto_scan = opened

            if self._auto_scan:
                self.scan()

        super().__init__(
            title="Wi-Fi",
            subtitle=device.ap.bind_many(
                ["is_connected", "ssid"], lambda a, b: subtitle(a, b)
            ),
            icon_name=device.ap.bind("icon-name", lambda v: v),
            on_activate=lambda _: network.wifi.set_enabled(True),
            on_deactivate=lambda _: network.wifi.set_enabled(False),
            active=network.wifi.bind("enabled"),
            menu=WifiMenu(device),
        )
        self.menu.connect(
            "notify::reveal-child", lambda v, _: on_opened(v.reveal_child)
        )

        utils.Poll(2000, lambda _: self._auto_scan and self.scan())

    def scan(self):
        if network.wifi.enabled:
            asyncio.create_task(self._device.scan())


def wifi_control() -> list[QSButton]:
    return [WifiQS(dev) for dev in network.wifi.devices]
